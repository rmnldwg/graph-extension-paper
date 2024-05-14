"""
Plot histograms of predicted risks, given different diagnoses.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, draw
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


INPUT = paths.data / "wg_risks.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 2, 2


def add_row_label(ax, label, pad=30):
    _ax = ax.secondary_yaxis("left")
    _ax.tick_params(axis="y", left=False, labelleft=False)
    _ax.set_ylabel(label, fontweight="bold", labelpad=pad)


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.45,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, sharex="col", sharey="row")

    left_panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        left_panels[stage] = [
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/IV/N0",
                label="given N0",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/IV/II",
                label="given LNL II involved",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/IV/IIandIII",
                label="given LNL II & III involved",
                color=USZ["orange"],
            ),
        ]

    draw(axes[0,0], contents=left_panels["early"], xlims=(0., 7.), hist_kwargs={"nbins": 40})
    axes[0,0].set_title("...in LNL IV", fontsize="medium", fontweight="bold")
    axes[0,0].set_ylabel("density")
    axes[0,0].legend(title="Diagnosis", title_fontsize="x-small", labelspacing=0.3)
    add_row_label(axes[0,0], "early T-cat.")

    draw(axes[1,0], contents=left_panels["late"], xlims=(0., 7.), hist_kwargs={"nbins": 40})
    axes[1,0].set_ylabel("density")
    axes[1,0].set_xlabel("risk [%]")
    add_row_label(axes[1,0], "early T-cat.")

    right_panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        right_panels[stage] = [
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/V/N0",
                label="N0",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/V/IIandIII",
                label="LNL II & III involved",
                color=USZ["orange"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/V/IIandIIIandIV",
                label="LNL II, III, IV involved",
                color=USZ["red"],
            ),
        ]

    draw(axes[0,1], contents=right_panels["early"], xlims=(0., 6.), hist_kwargs={"nbins": 40})
    axes[0,1].set_title("...in LNL V", fontsize="medium", fontweight="bold")
    axes[0,1].legend(title="Diagnosis", title_fontsize="x-small", labelspacing=0.3)

    draw(axes[1,1], contents=right_panels["late"], xlims=(0., 6.), hist_kwargs={"nbins": 40})
    axes[1,1].set_xlabel("risk [%]")

    fig.suptitle("Predicted risk of involvement...", fontsize="medium", fontweight="bold")
    plt.savefig(OUTPUT, dpi=300)
