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
    output:
        "src/tex/output/results_table.tex"
    script:
        "src/scripts/compile_metrics_table.py"
