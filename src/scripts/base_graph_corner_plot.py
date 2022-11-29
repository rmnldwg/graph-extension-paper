"""
Render a corner plot of all 1D and 2D marginals of the sampled posterior distribution
over the spread parameters of the base graph model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from corner import corner
from emcee.backends import HDFBackend

import paths


INPUT = paths.data / "base_graph_samples.hdf5"
THIN = 10
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")


if __name__ == "__main__":
    # open samples
    backend = HDFBackend(paths.data / INPUT, read_only=True)
    samples = backend.get_chain(flat=True, thin=THIN)

    # create plot
    corner(samples)
    plt.savefig(OUTPUT, dpi=300)
