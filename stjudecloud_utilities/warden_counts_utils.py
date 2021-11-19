"""This script has multiple utilities to work with HTSeq count files.

Of particular note, the `header` subcommand can be used to add a header to HTSeq count
files so that they can be used by WARDEN. The logic is simple: it adds a constant column
name for the gene name and then looks at the file name to add the sample column.

Further, the `samplesheet` subcommand can be used to quickly bootstrap up a WARDEN
samplesheet.
"""

import argparse
import os

from glob import glob
from typing import List
from itertools import combinations

def main():
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    header = subparsers.add_parser("header", description="Headers an HTSeq count file for use in WARDEN.")
    header.add_argument("input_file", help="HTSeq-count file to add a header to.")
    header.add_argument("output_file", help="File to write the result to.")
    header.add_argument(
        "-g", "--gene-column-name",
        default="Gene",
        help="Constant value to set the gene column to."
    )

    samplesheet = subparsers.add_parser("samplesheet", description="Prepares a samplesheet for WARDEN.")
    samplesheet.add_argument("output_file", help="File to write the result to.")
    samplesheet.add_argument("-d", "--dirs", nargs="+", required=True, help="Directories containing samples within their respective groups.")

    args = parser.parse_args()
    kwargs = vars(args)
    globals()[kwargs.pop('subcommand')](**kwargs)

def samplename_from_file(filename: str):
    return os.path.basename(filename).split(".")[0] if "." in filename else filename

def header(
    input_file: str, output_file: str, gene_column_name: str
):
    sample_name = samplename_from_file(input_file)

    with open(input_file, "r") as f:
        contents = f.read()

    parent_dir = os.path.dirname(output_file)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    with open(output_file, "w") as f:
        f.write(f"{gene_column_name}\t{sample_name}\n")
        f.write(contents)


def samplesheet(dirs: List[str], output_file: str):
    if not len(dirs) >= 2:
        raise RuntimeError("Must have at least two groups to create a samplesheet for!")

    for dir in dirs:
        if not os.path.isdir(dir):
            raise RuntimeError(f"{dir} is not a directory.")

        if "-" in dir:
            raise RuntimeError(f"Folders cannot have a dash in the name: {dir}")

        if "," in dir:
            raise RuntimeError(f"Folders cannot have a comma in the name: {dir}")


    with open(output_file, "w") as f:
        f.write("Sample\tPhenotype\tReadfile1\tReadfile2\n")
        for dir in dirs:
            for detected_file in glob(dir + "/*"):
                bn = os.path.basename(detected_file)
                sample_name = samplename_from_file(bn)
                f.write(f"{sample_name}\t{dir}\t{bn}\t-\n")

        f.write("#comparisons=")
        f.write(",".join([x + "-" + y for (x, y) in combinations(dirs, 2)]))


if __name__ == "__main__":
    main()
