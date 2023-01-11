rule get_dvc_files:
    input:
        "src/scripts/{filename}.dvc"
    output:
        "src/data/{filename}"
    shell:
        "dvc update {input}"

rule compute_prevalences:
    input:
        data = "src/data/patients.csv",
        model = "src/data/{graph}_samples.hdf5",
        params = "src/scripts/{graph}_{name}_params.yaml",
    output:
        "src/data/{graph}_{name}_prevs.hdf5"
    shell:
        "lyscripts predict prevalences --params {input.params} --thin 10 {input.model} {input.data} {output}"

rule extract_metrics:
    input:
        "src/data/bg_metrics.json",
        "src/data/wg_metrics.json",
        "src/scripts/results_table.temp",
    output:
        "src/tex/output/results_table.tex"
    script:
        "src/scripts/compile_metrics_table.py"

rule compile_data_table:
    input:
        "src/data/bg_core_prevs.hdf5",
        "src/data/bg_IandII_prevs.hdf5",
        "src/data/wg_IandII_prevs.hdf5",
        "src/data/bg_IandII_prevs.hdf5",
        "src/data/wg_IandII_prevs.hdf5",
        "src/data/bg_IIandVII_prevs.hdf5",
        "src/data/wg_IIandVII_prevs.hdf5",
        "src/data/bg_IIIandV_prevs.hdf5",
        "src/data/wg_IIIandV_prevs.hdf5",
        "src/data/bg_IVandV_prevs.hdf5",
        "src/data/wg_IVandV_prevs.hdf5",
        "src/scripts/data_table.temp",
    output:
        "src/tex/output/data_table.tex"
    script:
        "src/scripts/compile_data_table.py"

rule get_num_patients:
    input:
        "src/data/patients.csv",
    output:
        "src/tex/output/num_patients.txt",
    script:
        "src/scripts/get_num_patients.py"
