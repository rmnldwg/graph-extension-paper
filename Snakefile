rule get_hdf5_files:
    input:
        "src/scripts/{filename}.hdf5.dvc"
    output:
        "src/data/{filename}.hdf5"
    shell:
        "dvc update {input}"

rule compute_prevalences:
    input:
        data = "src/data/patients.csv",
        model = "src/data/{graph}_samples.hdf5",
        params = "src/scripts/{graph}_params.yaml",
    output:
        "src/data/{graph}_prevalences.hdf5"
    shell:
        "lyscripts predict prevalences --params {input.params} --thin 10 {input.model} {input.data} {output}"
    