"""
Populate a Jinja2 LaTeX table template with the metrics from the experiment runs.
"""
import json

import pandas as pd
import matplotlib.pyplot as plt
from lyscripts.plot.utils import COLORS as USZ
from dvc.api import DVCFileSystem

import paths


REVISIONS = {
    "base-graph-v2": "base graph",
    "add-I-to-II": "add I → II",
    "add-I-to-II-and-III-to-V": "add I → II & III → V",
    "add-I-to-II-and-III-to-V-and-IV-to-V": "add I → II & III → V & IV → V",
    "add-I-to-II-and-IV-to-V": "add I → II & IV → V",
    "add-II-to-I": "add II → I",
    "add-II-to-V": "add II → V",
    "add-II-to-VII": "add II → VII",
    "add-III-to-V": "add III → V",
    "add-IV-to-V": "add IV → V",
    "del-II-to-III": "remove II → III",
    "del-II-to-III-and-III-to-IV": "remove II → III & III → IV",
    "del-III-to-IV": "remove III → IV",
}

TABLE_OUTPUT = paths.output / "results_table.tex"
VISUAL_OUTPUT = paths.figures / "visual_ranking_guide.svg"


if __name__ == "__main__":
    evidences = []

    for revision in REVISIONS.keys():
        dvc_filesystem = DVCFileSystem(
            url="https://github.com/rmnldwg/lynference",
            rev=revision,
        )

        with dvc_filesystem.open("metrics.json") as f:
            metrics = json.load(f)

        evidences.append(metrics["evidence"])

    results = pd.DataFrame.from_dict({
        "graph": REVISIONS.values(),
        "evidence": evidences,
    }).sort_values(by="evidence", ascending=False)

    with open(TABLE_OUTPUT, "w") as f:
        f.write(results.to_latex(index=False, escape=True, float_format="%.2f"))

    fig, ax = plt.subplots(figsize=(10,1))
    ax.plot(
        results["evidence"][:-2],
        [0] * (len(results) - 2), "o",
        color=USZ["blue"],
    )

    # disable everything except the plottet points
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.savefig(VISUAL_OUTPUT, bbox_inches="tight")
