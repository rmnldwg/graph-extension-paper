rule get_base_graph_samples:
    output:
        "src/data/base_graph_samples.hdf5"
    shell:
        "dvc update {output}.dvc"

rule get_base_graph_prevalences:
    output:
        "src/data/base_graph_prevalences.hdf5"
    shell:
        "dvc update {output}.dvc"
