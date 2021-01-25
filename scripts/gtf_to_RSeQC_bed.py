import gzip
import sys
import itertools
import re
from typing import DefaultDict

if not sys.argv[1]:
    print("Missing GTF!")
    raise SystemExit(1)

filename = sys.argv[1]
gzipped = False
if "gz" in filename.split(".")[-1]:
    handle = gzip.open(filename)
    gzipped = True
else:
    handle = open(filename, "r")


class Tx:
    def __init__(self, tx_start=None, tx_end=None, contig=None):
        self.start = tx_start
        self.end = tx_end
        self.contig = contig
        self.strand = None
        self.starts = []
        self.ends = []


attr_regexes = [r"(\S+)=(\S+)", r"(\S+) \"(\S+)\""]
transcripts = DefaultDict(Tx)
for line in handle:
    if gzipped:
        line = line.decode("utf-8")
    if line[0] == "#":
        continue
    [
        seqname,
        source,
        feature,
        start,
        end,
        score,
        strand,
        frame,
        attribute,
    ] = line.split("\t")

    if feature != "transcript" and feature != "exon":
        continue
    attribute = attribute.replace(';"', '"').replace(
        ";-", "-"
    )  # correct error in ensemble 78 release
    attributes = {}
    for attr_raw in [s.strip() for s in attribute.split(";")]:
        if not attr_raw or attr_raw == "":
            continue

        for regex in attr_regexes:
            match = re.match(regex, attr_raw)
            if match:
                key, value = match.group(1), match.group(2)
                attributes[key.strip()] = value.strip()

    tx = transcripts[  # pylint: disable=unsubscriptable-object
        attributes["transcript_id"]
    ]
    if feature == "transcript":
        assert tx.start is None
        tx.start = int(start) - 1
        tx.end = int(end)
        tx.contig = seqname
        if tx.strand:
            assert tx.strand == strand
        tx.strand = strand
    else:
        tx.starts.append(int(start) - 1)
        tx.ends.append(int(end))
        if tx.strand:
            assert tx.strand == strand

for tx_name, tx in transcripts.items():  # pylint: disable=no-member
    print(
        "\t".join(
            [
                tx.contig,
                str(tx.start),
                str(tx.end),
                tx_name,
                "0",
                tx.strand,
                ".",
                ".",
                ".",
                str(len(tx.starts)),
            ]
        ),
        end="\t",
    )
    sizes = [str(end - start) for start, end in zip(tx.starts, tx.ends)]
    starts = [str(start - tx.start) for start in tx.starts]
    print(",".join(sizes), end="\t")
    print(",".join(starts))
