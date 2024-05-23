"""
Populate a Jinja2 LaTeX table template with the metrics from the experiment runs.
"""
import json
from jinja2 import Environment, FileSystemLoader

import pandas as pd
import matplotlib.pyplot as plt
from lyscripts.plot.utils import COLORS as USZ
from dvc.api import DVCFileSystem

import paths


REVISIONS = {
    "base-graph-v2": "base graph",
    "add-I-to-II": "add I → II",
    "add-I-to-II-and-III-to-V": "add I → II \& III → V",
    "add-I-to-II-and-III-to-V-and-IV-to-V": "add I → II \& III → V \& IV → V",
    "add-I-to-II-and-IV-to-V": "add I → II \& IV → V",
    "add-II-to-I": "add II → I",
    "add-II-to-V": "add II → V",
    "add-II-to-VII": "add II → VII",
    "add-III-to-V": "add III → V",
    "add-IV-to-V": "add IV → V",
    "del-II-to-III": "remove II → III",
    "loose-graph-v1": "remove II → III \& III → IV",
    "del-III-to-IV": "remove III → IV",
}

TEMPLATE_NAME = "metrics_table.temp"
TABLE_OUTPUT = paths.output / "metrics_table.tex"
VISUAL_OUTPUT = paths.figures / "visual_ranking_guide.svg"


if __name__ == "__main__":
    results = []

    dvc_filesystem = DVCFileSystem(
        url="https://github.com/rmnldwg/lynference",
        rev="base-graph-v2",
    )
    with dvc_filesystem.open("metrics.json") as f:
        metrics = json.load(f)
    baseline = metrics["evidence"]

    for revision, graph in REVISIONS.items():
        dvc_filesystem = DVCFileSystem(
            url="https://github.com/rmnldwg/lynference",
            rev=revision,
        )

        with dvc_filesystem.open("metrics.json") as f:
            metrics = json.load(f)

        results.append({
            "graph": graph,
            "evidence": metrics["evidence"] - baseline,
        })

    sorted_results = sorted(results, key=lambda x: x["evidence"], reverse=True)

    environment = Environment(loader=FileSystemLoader(paths.scripts))
    template = environment.get_template(TEMPLATE_NAME)

    with open(TABLE_OUTPUT, "w") as f:
        f.write(template.render(results=sorted_results))

    # fig, ax = plt.subplots(figsize=(10,1))
    # ax.plot(
    #     results["evidence"][:-2],
    #     [0] * (len(results) - 2), "o",
    #     color=USZ["blue"],
    # )

    # # disable everything except the plottet points
    # ax.set_xticks([])
    # ax.set_yticks([])
    # ax.spines["right"].set_visible(False)
    # ax.spines["top"].set_visible(False)
    # ax.spines["left"].set_visible(False)
    # ax.spines["bottom"].set_visible(False)

    # plt.savefig(VISUAL_OUTPUT, bbox_inches="tight")
