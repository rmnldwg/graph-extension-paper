"""
Plot histograms of predicted and posteriors over observed prevalences for scenarios
that involve the LNL VII. Compare these prevalence predictions for the base-graph
model to the winning-graph model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


BASE_GRAPH_INPUT = paths.data / "bg_VII_prevs.hdf5"
WIN_GRAPH_INPUT = paths.data / "wg_VII_prevs.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 1, 2


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_half(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.3,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS)


    panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        panels[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"VII/{stage}",
                label="LNL VII overall",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VII/{stage}",
                label="base graph",
                histtype="step",
                color="darkgray",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VII/{stage}",
                color=USZ["blue"],
            ),
        ]

    draw(axes[0], contents=panels["early"], xlims=(2., 10.), hist_kwargs={"nbins": 40})
    h, l = axes[0].get_legend_handles_labels()
    handles = [*h[2:4], h[0], *h[4:6], h[1]]
    labels = [*l[2:4], l[0], *l[4:6], l[1]]
    axes[0].set_ylim(bottom=0.)
    axes[0].set_title("early T-cat.", fontweight="bold")
    axes[0].set_yticks([])
    axes[0].legend(handles=handles, labels=labels)

    draw(axes[1], contents=panels["late"], xlims=(4., 12.), hist_kwargs={"nbins": 40})
    h, l = axes[1].get_legend_handles_labels()
    handles = h[:2]
    labels = l[:2]
    axes[1].set_ylim(bottom=0.)
    axes[1].set_title("late T-cat.", fontweight="bold")
    axes[1].set_yticks([])
    axes[1].set_xlabel("prevalence [%]")
    axes[1].legend(handles=handles, labels=labels)

    plt.savefig(OUTPUT, dpi=300)
