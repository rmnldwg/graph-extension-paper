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
NROWS, NCOLS = 2, 1


def add_row_label(ax, label, pad=30):
    _ax = ax.secondary_yaxis("left")
    _ax.tick_params(axis="y", left=False, labelleft=False)
    _ax.set_ylabel(label, fontweight="bold", labelpad=pad)


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_half(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.45,
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
                dataname=f"{stage}/III/N0",
                label="N0",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/III/II",
                label="LNL II involved",
                color=USZ["blue"],
            ),
        ]

    draw(axes[0], contents=panels["early"], xlims=(0., 15.), hist_kwargs={"nbins": 40})
    axes[0].set_ylabel("density")
    add_row_label(axes[0], "early T-cat.")

    draw(axes[1], contents=panels["late"], xlims=(0., 15.), hist_kwargs={"nbins": 40})
    axes[1].set_ylabel("density")
    axes[1].set_xlabel("risk [%]")
    axes[1].legend(title="Diagnosis", title_fontsize="x-small", labelspacing=0.3)
    add_row_label(axes[1], "late T-cat.")

    fig.suptitle("Predicted risk of involvement in LNL III", fontsize="medium", fontweight="bold")
    plt.savefig(OUTPUT, dpi=300)
