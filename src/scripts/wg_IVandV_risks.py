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
                label="LNL IV, given N0",
                color=USZ["green"],
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

    draw(axes[0,0], contents=left_panels["early"], xlims=(0., 7.), hist_kwargs={"nbins": 40})
    axes[0,0].set_ylabel("early T-cat.", fontweight="bold")
    axes[0,0].set_yticks([])
    axes[0,0].legend()

    draw(axes[1,0], contents=left_panels["late"], xlims=(0., 7.), hist_kwargs={"nbins": 40})
    axes[1,0].set_ylabel("late T-cat.", fontweight="bold")
    axes[1,0].set_yticks([])
    axes[1,0].set_xlabel("risk [%]")

    right_panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        right_panels[stage] = [
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/V/N0",
                label="LNL V, given N0",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/V/IIandIII",
                label="LNL V, given LNL II & III involved",
                color=USZ["orange"],
            ),
            Histogram.from_hdf5(
                filename=INPUT,
                dataname=f"{stage}/V/IIandIIIandIV",
                label="LNL V, given LNL II, III, IV involved",
                color=USZ["red"],
            ),
        ]

    draw(axes[0,1], contents=right_panels["early"], xlims=(0., 6.), hist_kwargs={"nbins": 40})
    axes[0,1].set_yticks([])
    axes[0,1].legend()

    draw(axes[1,1], contents=right_panels["late"], xlims=(0., 6.), hist_kwargs={"nbins": 40})
    axes[1,1].set_yticks([])
    axes[1,1].set_xlabel("risk [%]")

    plt.savefig(OUTPUT, dpi=300)
