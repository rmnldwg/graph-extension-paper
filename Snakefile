rule get_dvc_files:
    input:
        "src/scripts/{filename}.dvc"
    output:
        "src/data/{filename}"
    shell:
        "dvc update --verbose {input}"

rule compute_prevalences:
    input:
        data = "src/data/patients.csv",
        model = "src/data/{graph}_samples.hdf5",
        params = "src/scripts/{graph}_{name}_params.yaml"
    output:
        "src/data/{graph}_{name}_prevs.hdf5"
    shell:
        "lyscripts predict prevalences --params {input.params} {input.model} {input.data} {output}"

rule compute_risks:
    input:
        model = "src/data/{graph}_samples.hdf5",
        params = "src/scripts/{graph}_risks.yaml"
    output:
        "src/data/{graph}_risks.hdf5"
    shell:
        "lyscripts predict risks --params {input.params} {input.model} {output}"

rule compile_metrics_table:
    input:
        "src/data/bg_metrics.json",
        "src/data/wg_metrics.json",
        "src/scripts/metrics_table.temp"
    output:
        "src/tex/output/metrics_table.tex"
    script:
        "src/scripts/compile_metrics_table.py"

rule compile_data_table:
    input:
        "src/data/bg_core_prevs.hdf5",
        "src/data/bg_IandII_prevs.hdf5",
        "src/data/wg_IandII_prevs.hdf5",
        "src/data/bg_IIandVII_prevs.hdf5",
        "src/data/wg_IIandVII_prevs.hdf5",
        "src/data/bg_IIIandV_prevs.hdf5",
        "src/data/wg_IIIandV_prevs.hdf5",
        "src/data/bg_IVandV_prevs.hdf5",
        "src/data/wg_IVandV_prevs.hdf5",
        "src/scripts/data_table.temp"
    output:
        "src/tex/output/data_table.tex"
    script:
        "src/scripts/compile_data_table.py"

rule get_num_patients:
    input:
        "src/data/patients.csv"
    output:
        "src/tex/output/num_patients.txt"
    script:
        "src/scripts/get_num_patients.py"

rule compile_means_table:
    input:
        "src/data/wg_samples.hdf5",
        "src/scripts/means_table.temp"
    output:
        "src/tex/output/means_table.tex"
    script:
        "src/scripts/compile_means_table.py"

rule write_wg_II_risk:
    input:
        "src/data/wg_risks.hdf5"
    output:
        "src/tex/output/wg_II_risks.tex"
    script:
        "src/scripts/wg_II_risks.py"

rule write_evidence_diff:
    input:
        "src/data/wg_metrics.json",
        "src/data/lg_metrics.json"
    output:
        "src/tex/output/evidence_diff.txt"
    script:
        "src/scripts/evidence_diff.py"
