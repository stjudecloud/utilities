#!/usr/bin/env python3

import argparse
import json
import sys
from typing import List
from subprocess import check_output
from collections import defaultdict

store = defaultdict(list)

LOG = False
BAD_FILES_FOLDER = "/bad-files/"
PRIORITIES = [
    "Clinical Pilot",
    "Pediatric Cancer Genome Project (PCGP)",
    "Real Time Clinical Genomics (RTCG)",
    "Genomes 4 Kids (G4K)",
    "Childhood Solid Tumor Network (CSTN)",
    "Pan-Acute Lymphoblastic Leukemia (PanALL)",
    "Pediatric Therapy-related Myeloid Neoplasms (tMN)",
    "Pediatric Brain Tumor Program (PBTP)",
    "Pediatric Acute Myeloid Leukemia (PedAML)",
    "Genomics and transcriptomics of relapsed pediatric AML (RPAML)",
]


def simple_log(msg: str = ""):
    if LOG:
        sys.stderr.write(f"LOG: {msg}\n")
        sys.stderr.flush()


def simple_error(msg: str, suggest_contact: bool = True):
    sys.stderr.write(f"\n\nERROR: {msg}")
    if suggest_contact:
        sys.stderr.write(" Please contact us at support@stjude.cloud with this error.")
    sys.stderr.flush()
    sys.exit(1)


def get_best_file(
    fn: str, file_ids: List[str], priority_list: List[str] = PRIORITIES
) -> str:
    """Gets the best file given the dataset priorities given in priorities

    Args:
        file_id (List[str]): list of DNAnexus file ids that have a similar name.
        priorities (List[str]): list of datasets to prioritize

    Raises:
        RuntimeError: file does not have the correct properties annotated.

    Returns:
        str: best file id to use based on priority_list
    """

    file_id_to_datasets = {}
    for fid in file_ids:
        full_describe = check_output(f"dx describe {fid} --json", shell=True)
        datasets = json.loads(full_describe).get("properties", {}).get("sj_datasets")
        if not datasets:
            raise RuntimeError(
                f"File {fid} doesn't have the correct properties annotated! "
                + "Did you get this file from St. Jude Cloud? If so, please "
                + "contact us with this error at support@stjude.cloud.",
                suggest_contact=False,
            )

        file_id_to_datasets[fid] = set([e.strip() for e in datasets.split(";")])

    # first, ensure every file belongs to *at least* one dataset above.
    # if any file belongs to a new dataset, then out of an abundance of
    # caution, we will error and ask the user to explicitly add that
    # dataset to the priority_list list.

    for file_id, datasets in file_id_to_datasets.items():
        if not any([dataset in priority_list for dataset in datasets]):
            simple_error(
                f"File {fid} doesn't contain a dataset tag in the known priority "
                + "list. This likely means that a new dataset has been released "
                + "to St. Jude Cloud since this script was written. Out of an "
                + "abundance of caution, we ask that you explicitly "
                + "update the PRIORITIES variable at the top of this script to "
                + f"include one of the following values: {datasets}. "
                + "\n\nWe would also appreciate it if you reached out to us at "
                + "support@stjude.cloud with this error so we can fix it for future "
                + "users.",
                suggest_contact=False,
            )

    simple_log()
    simple_log(f"== {fn} ==")

    hooked_file = None
    for candidate_dataset in priority_list:
        simple_log(f'  [*] Looking for dataset "{candidate_dataset}".')
        for file_id, actual_datasets in file_id_to_datasets.items():
            contains = any([e == candidate_dataset for e in actual_datasets])
            simple_log(f"    - {file_id} => {actual_datasets} (contains: {contains})")
            if contains:
                if not hooked_file:
                    hooked_file = file_id
                else:
                    # a file that was attached to this dataset already existed, and now we've found
                    # a second one. I don't expect this to ever happen in practice (two files in the
                    # same dataset with the same name), so if it does, we should email support@stjude.cloud
                    simple_error(
                        f"More than one file id had the same dataset and same name: {file_id_to_datasets}."
                        + "This is unexpected."
                    )

        if hooked_file:
            simple_log(f"    - Found file in {candidate_dataset}: {hooked_file}.")
            break

    if not hooked_file:
        raise simple_error(
            f"No files with datasets in the priority list were found: {file_id_to_datasets}."
        )

    return hooked_file


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicates samples in DNAnexus based on the project priority " + \
             "the St. Jude Cloud team uses."
    )
    parser.add_argument("dxids", nargs="+", type=str, help="DNAnexus file ids to deduplicate")
    args = parser.parse_args()

    for line in [l.strip() for l in args.dxids]:
        if ":" not in line:
            continue

        fn, fid = [s.strip() for s in line.split(":")]
        store[fn].append(fid)

    print(f"dx mkdir {BAD_FILES_FOLDER}")
    for fn, fids in store.items():
        best_file_id = get_best_file(fn, fids)
        files_to_remove = fids.copy()
        files_to_remove.remove(best_file_id)
        print(f"dx mv {' '.join(list(files_to_remove))} {BAD_FILES_FOLDER}")

if __name__ == "__main__":
    main()