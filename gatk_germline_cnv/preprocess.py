#!/usr/bin/env python3

import json
from cirro.helpers.preprocess_dataset import PreprocessDataset
from cirro.api.models.s3_path import S3Path

def mark_filetype(fp: str) -> str:
    if fp.endswith(".bam"):
        return "bam"
    elif fp.endswith(".bai"):
        return "bai"
    else:
        return "other"

def setup_inputs(ds: PreprocessDataset):
    # turn comma separated string of bam_files into list
    ds.params[
        "CNVGermlineCohortWorkflow.normal_bams"
    ] = ds.params.get(
        "CNVGermlineCohortWorkflow.normal_bams",
        "bam_files"
    ).split(',')

    # turn comma separated string of normal_bais into list with .bai suffix
    ds.params[
        "CNVGermlineCohortWorkflow.normal_bams"
    ] = [x + ".crai" for x in ds.params.get(
        "CNVGermlineCohortWorkflow.normal_bams",
        "bai_files"
    ).split(',')]

    all_inputs = {
                kw: val
                for kw, val in ds.params.items()
                if kw.startswith("CNVGermlineCohortWorkflow")
            }

    # Write out the complete set of inputs
    write_json("inputs.json", all_inputs)

    # Write out each individual file pair
    write_json(f"inputs.0.json", all_inputs)


def write_json(fp, obj, indent=4) -> None:

    with open(fp, "wt") as handle:
        json.dump(obj, handle, indent=indent)


def setup_options(ds: PreprocessDataset):

    # Add default params
    ds.add_param("memory_retry_multiplier", 2.0)
    ds.add_param("use_relative_output_paths", True)

    # Set up the scriptBucketName
    ds.add_param(
        "scriptBucketName",
        S3Path(ds.params['final_workflow_outputs_dir']).bucket
    )

    # Isolate the options arguments for the workflow
    options = {
        kw: val
        for kw, val in ds.params.items()
        if not kw.startswith("CNVGermlineCohortWorkflow")
    }

    # Write out
    with open("options.json", "wt") as handle:
        json.dump(options, handle, indent=4)


if __name__ == "__main__":
    ds = PreprocessDataset.from_running()
    setup_inputs(ds)
    setup_options(ds)


