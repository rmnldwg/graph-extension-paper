rule get_hdf5_files:
    input:
        "src/scripts/{filename}.hdf5.dvc"
    output:
        "src/data/{filename}.hdf5"
    shell:
        "dvc update {input}"
