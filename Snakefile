rule extended_base_v1_samples:
    output:
        "src/data/extended-base-v1-samples.hdf5"
    shell:
        "dvc update src/scripts/extended-base-v1-samples.hdf5.dvc"
