"""
Plot histograms of predicted and posteriors over observed prevalences for high-risk
scenarios as computed by models with different arcs between LNL I and II.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw, COLORS, get_size

import paths
from constants import linewidth_in_cm


BASE_GRAPH = paths.data / "base_graph_prevalences.hdf5"
ADD12 = paths.data / "add12_prevalences.hdf5"
ADD21 = paths.data / "add21_prevalences.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")


if __name__ == "__main__":
    fig, axes = plt.subplots(figsize=get_size(width=linewidth_in_cm))

    early_12_panel = [
        Histogram.from_hdf5(
            filename=BASE_GRAPH,
            dataname="I/early",
            color="gray",
            hatch=r"////",
        ),
        Histogram.from_hdf5(
            filename=BASE_GRAPH,
            dataname="InotII/early",
            color="gray",
            hatch=r"\\\\",
        ),
        Histogram.from_hdf5(
            filename=ADD12,
            dataname="I/early",
            color=COLORS["blue"],
        ),
        Histogram.from_hdf5(
            filename=ADD12,
            dataname="InotII/early",
            color=COLORS["green"],
        ),
    ]

    draw(axes, contents=early_12_panel)
    plt.savefig(OUTPUT, dpi=400)
