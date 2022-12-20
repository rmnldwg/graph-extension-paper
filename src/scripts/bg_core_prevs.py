"""
Plot histograms of predicted and posteriors over observed prevalences for basic
scenarios involving the LNLs II, III and IV. This is to show that the base graph is
already capable of capturing the frequency of these involvement, as well as their
correlations.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw, COLORS
from tueplots import figsizes, fontsizes

import paths


INPUT = paths.data / "bg_core_prevs.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 2, 1


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.3,
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
                filename=INPUT,
                dataname=f"II/{stage}",
                label="LNL II overall",
                color=COLORS["red"],
            ),
            Posterior.from_hdf5(
                filename=INPUT,
                dataname=f"II/{stage}",
                color=COLORS["red"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"III/{stage}",
                label="LNL III overall",
                color=COLORS["blue"],
            ),
            Posterior.from_hdf5(
                filename=INPUT,
                dataname=f"III/{stage}",
                color=COLORS["blue"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"IV/{stage}",
                label="LNL IV overall",
                color=COLORS["green"],
            ),
            Posterior.from_hdf5(
                filename=INPUT,
                dataname=f"IV/{stage}",
                color=COLORS["green"],
            ),
        ]

    panels["early"].append(Histogram.from_hdf5(
        filename=INPUT,
        dataname="IInotIII/early",
        label="LNL II without LNL III",
        color=COLORS["orange"],
    ))
    panels["early"].append(Posterior.from_hdf5(
        filename=INPUT,
        dataname="IInotIII/early",
        color=COLORS["orange"],
    ))

    panels["late"].append(Histogram.from_hdf5(
        filename=INPUT,
        dataname="IIInotIV/late",
        label="LNL III without LNL IV",
        color="#8f8f8f",
    ))
    panels["late"].append(Posterior.from_hdf5(
        filename=INPUT,
        dataname="IIInotIV/late",
        color="#8f8f8f",
    ))
    panels["late"].append(Histogram.from_hdf5(
        filename=INPUT,
        dataname="IIIandIV/late",
        label="LNL III and LNL IV",
        histtype="step",
        color="black",
        linewidth=2.,
        hatch=r"////",
    ))
    panels["late"].append(Posterior.from_hdf5(
        filename=INPUT,
        dataname="IIIandIV/late",
        color="black",
    ))

    draw(axes[0], contents=panels["early"], xlims=(0., 85.), hist_kwargs={"nbins": 120})
    axes[0].set_ylabel("early T-cat.", fontweight="bold")
    axes[0].legend(loc="upper right")

    draw(axes[1], contents=panels["late"], xlims=(0., 85.), hist_kwargs={"nbins": 120})
    axes[1].set_ylabel("late T-cat.", fontweight="bold")
    axes[1].set_xlabel("prevalence [%]")
    axes[1].legend(handles=axes[1].get_children()[5:10],)

    plt.savefig(OUTPUT, dpi=300)
