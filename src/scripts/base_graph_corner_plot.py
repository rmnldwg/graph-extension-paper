"""
Render a corner plot of all 1D and 2D marginals of the sampled posterior distribution
over the spread parameters of the base graph model.
"""
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from corner import corner
from emcee.backends import HDFBackend

import paths


class Namespace:
    """Make script runnable without snakemake by creating a simple namespace."""
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(**kwargs)


# if "snakemake" not in locals():
#     warnings.warn("Snakemake did not provide params.")
#     snakemake = Namespace(
#         input=paths.data / "base_graph_samples.hdf5",
#         thin=10,
#         output=paths.figures / Path(__file__).with_suffix(".png")
#     )


if __name__ == "__main__":
    # open samples
    backend = HDFBackend(paths.data / snakemake.input, read_only=True)
    samples = backend.get_chain(flat=True, thin=snakemake.thin)

    # create plot
    corner(samples)
    plt.savefig(snakemake.output, dpi=300)
