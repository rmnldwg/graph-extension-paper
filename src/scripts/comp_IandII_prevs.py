"""
Plot histograms of predicted and posteriors over observed prevalences for scenarios
that involve the LNLs I and II. Compare these prevalence predictions for the base-graph
model to the winning-graph model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


BASE_GRAPH_INPUT = paths.data / "bg_IandII_prevs.hdf5"
WIN_GRAPH_INPUT = paths.data / "wg_IandII_prevs.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 2, 1


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_half(
        nrows=NROWS,
        ncols=NCOLS,
        # height_to_width_ratio=0.3,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, sharex="col", sharey="row")

    panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        panels[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"I/{stage}",
                label="LNL I overall",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"I/{stage}",
                label="base graph",
                histtype="step",
                color="darkgray",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"I/{stage}",
                color=USZ["blue"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"InotII/{stage}",
                label="LNL I without II",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"InotII/{stage}",
                label="base graph",
                histtype="step",
                color="darkgray",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"InotII/{stage}",
                color=USZ["green"],
            ),
        ]

    draw(axes[0], contents=panels["early"], xlims=(0., 15.), hist_kwargs={"nbins": 40})
    axes[0].set_ylim(bottom=0., top=1.5)
    axes[0].set_ylabel("early T-cat.", fontweight="bold")
    axes[0].legend()

    draw(axes[1], contents=panels["late"], xlims=(0., 15.), hist_kwargs={"nbins": 40})
    axes[1].set_ylim(bottom=0., top=1.2)
    axes[1].set_ylabel("late T-cat.", fontweight="bold")
    axes[1].set_xlabel("prevalence [%]")
    axes[1].legend(handles=axes[1].get_children()[2:6:3],)

    plt.savefig(OUTPUT, dpi=300)
