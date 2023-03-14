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
                dataname=f"{stage}/IV/N0",
                label=None,
                color=USZ["gray"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/IV/N0",
                label="LNL IV, given N0",
                color="#97a3a7",
                histtype="step",
                linewidth=2.,
                alpha=1.0,
                zorder=1.,
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/IV/II",
                label="LNL IV, given LNL II involved",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/IV/IIandIII",
                label="LNL IV, given LNL II & III involved",
                color=USZ["orange"],
            ),
        ]

    draw(axes[0], contents=panels["early"], xlims=(0., 7.), hist_kwargs={"nbins": 40})
    axes[0].set_ylabel("early T-cat.", fontweight="bold")
    axes[0].set_yticks([])
    axes[0].legend()

    draw(axes[1], contents=panels["late"], xlims=(0., 7.), hist_kwargs={"nbins": 40})
    axes[1].set_ylabel("late T-cat.", fontweight="bold")
    axes[1].set_yticks([])
    axes[1].set_xlabel("risk [%]")

    plt.savefig(OUTPUT, dpi=300)