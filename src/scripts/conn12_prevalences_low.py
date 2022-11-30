"""
Plot histograms of predicted and posteriors over observed prevalences for high-risk
scenarios as computed by models with different arcs between LNL I and II.
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw, COLORS
from tueplots import figsizes, fontsizes

import paths


BASE_GRAPH = paths.data / "base_graph_prevalences.hdf5"
ADD = {
    "12": paths.data / "add12_prevalences.hdf5",
    "21": paths.data / "add21_prevalences.hdf5",
}
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(nrows=2, ncols=2))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex="col", sharey="row")

    panels = {
        "early": {"12": [], "21": []},
        "late": {"12": [], "21": []},
    }

    for stage in ["early", "late"]:
        for direction in ["12", "21"]:
            panels[stage][direction] = [
                Histogram.from_hdf5(
                    filename=ADD[direction],
                    dataname=f"I/{stage}",
                    label="LNL I overall",
                    color=COLORS["blue"],
                ),
                Histogram.from_hdf5(
                    filename=BASE_GRAPH,
                    dataname=f"I/{stage}",
                    label="base graph",
                    color="black",
                    hatch=r"////",
                    histtype="step",
                    linewidth=1.5,
                    alpha=1.,
                ),
                Posterior.from_hdf5(
                    filename=ADD[direction],
                    dataname=f"I/{stage}",
                    color=COLORS["blue"],
                ),
                Histogram.from_hdf5(
                    filename=ADD[direction],
                    dataname=f"InotII/{stage}",
                    label="LNL I without II",
                    color=COLORS["green"],
                ),
                Histogram.from_hdf5(
                    filename=BASE_GRAPH,
                    dataname=f"InotII/{stage}",
                    label="base graph",
                    color="black",
                    hatch=r"\\\\",
                    histtype="step",
                    linewidth=1.5,
                    alpha=1.,
                ),
                Posterior.from_hdf5(
                    filename=ADD[direction],
                    dataname=f"InotII/{stage}",
                    color=COLORS["green"],
                ),
            ]

    draw(axes[0,0], contents=panels["early"]["12"], xlims=(0., 10.))
    axes[0,0].set_title("early T-category", fontweight="bold")
    axes[0,0].set_ylabel("I→II", fontweight="bold")
    axes[0,0].legend()

    draw(axes[1,0], contents=panels["early"]["21"], xlims=(0., 10.))
    axes[1,0].set_ylabel("II→I", fontweight="bold")
    axes[1,0].set_xlabel("prevalence [%]")

    draw(axes[0,1], contents=panels["late"]["12"], xlims=(0., 20.))
    axes[0,1].set_title("late T-category", fontweight="bold")
    axes[0,1].legend()

    draw(axes[1,1], contents=panels["late"]["21"], xlims=(0., 20.))
    axes[1,1].set_xlabel("prevalence [%]")
    axes[1,1].set_xticks(np.linspace(0., 20., 6))

    plt.savefig(OUTPUT, dpi=300)
