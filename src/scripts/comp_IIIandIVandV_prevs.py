"""
Plot histograms of predicted and posteriors over observed prevalences for scenarios
that involve the LNLs III, IV, and V. Compare these prevalence predictions for the
base-graph model to the winning-graph model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from lyscripts.plot.utils import Histogram, Posterior, draw
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 2, 2


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.45,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, sharex="col")

    # prevalences of LNLs IV and V
    BASE_GRAPH_INPUT = paths.data / "bg_IVandV_prevs.hdf5"
    WIN_GRAPH_INPUT = paths.data / "wg_IVandV_prevs.hdf5"

    panels_IVandV = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        panels_IVandV[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"IVandV/{stage}",
                label="LNL IV and V",
                color=USZ["orange"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IVandV/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"\\\\",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IVandV/{stage}",
                color=USZ["orange"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"VnotIV/{stage}",
                label="LNL V without IV",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIV/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIV/{stage}",
                color=USZ["blue"],
            ),
        ]

    # prevalences of III and V
    BASE_GRAPH_INPUT = paths.data / "bg_IIIandV_prevs.hdf5"
    WIN_GRAPH_INPUT = paths.data / "wg_IIIandV_prevs.hdf5"

    panels_IIIandV = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        panels_IIIandV[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"IIIandV/{stage}",
                label="LNL III and V",
                color=USZ["red"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IIIandV/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"\\\\",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IIIandV/{stage}",
                color=USZ["red"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"VnotIII/{stage}",
                label="LNL V without III",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIII/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIII/{stage}",
                color=USZ["green"],
            ),
        ]

    draw(axes[0,0], contents=panels_IIIandV["early"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    axes[0,0].set_ylim(bottom=0., top=1.0)
    axes[0,0].set_ylabel("early T-cat.", fontweight="bold")
    axes[0,0].set_yticks([])
    axes[0,0].legend()

    draw(axes[1,0], contents=panels_IIIandV["late"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    # axes[1,0].set_ylim(bottom=0., top=1.2)
    axes[1,0].set_ylabel("late T-cat.", fontweight="bold")
    axes[1,0].set_yticks([])
    axes[1,0].set_xlabel("prevalence [%]")
    axes[1,0].legend(handles=[h for h in axes[1,0].get_children() if isinstance(h, Line2D)])


    draw(axes[0,1], contents=panels_IVandV["early"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    axes[0,1].set_ylim(bottom=0., top=1.0)
    # axes[0,1].set_ylabel("early T-cat.", fontweight="bold")
    axes[0,1].set_yticks([])
    axes[0,1].legend()

    draw(axes[1,1], contents=panels_IVandV["late"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    # axes[1,1].set_ylim(bottom=0., top=1.2)
    # axes[1,1].set_ylabel("late T-cat.", fontweight="bold")
    axes[1,1].set_yticks([])
    axes[1,1].set_xlabel("prevalence [%]")
    axes[1,1].legend(handles=[h for h in axes[1,1].get_children() if isinstance(h, Line2D)])

    plt.savefig(OUTPUT, dpi=300)
