"""
Plot how the accuracies evolved for the lose vs the winning graph.
"""
from pathlib import Path

import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


ACCURACY_PATHS = {
    "lose": paths.data / "loose_accuracies.csv",
    "win" : paths.data / "win_accuracies.csv",
}
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
POWER = 3


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_half())
    plt.rcParams.update(fontsizes.icml2022())
    plt.rcParams.update({"text.usetex": False})
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)

    accuracies = pd.read_csv(
        ACCURACY_PATHS["lose"]
    ).rename(
        columns={"accuracy": "lose graph"}
    ).join(
        pd.read_csv(
            ACCURACY_PATHS["win"]
        ).rename(
            columns={"accuracy": "win graph"}
        ).drop(
            columns="β"
        ),
        lsuffix="_",
    )

    accuracies = accuracies.drop(columns=["std_", "std"])
    accuracies["β"] = accuracies["β"] ** (1./POWER)
    accuracies["diff"] = accuracies["win graph"] - accuracies["lose graph"]

    accuracies.plot(
        x="β",
        y="win graph",
        ax=axes[0],
        color=USZ["blue"],
        label="winning graph",
    )
    accuracies.plot(
        x="β",
        y="diff",
        ax=axes[1],
        color=USZ["red"],
        label="winning - losing graph",
    )
    axes[1].axhline(0., color="black", linestyle="--")

    xticks = np.linspace(0., 1., 7)
    xticklabels = [f"{x**POWER:.2g}" for x in xticks]

    axes[0].set_yscale("symlog",)
    axes[0].get_yaxis().set_major_locator(matplotlib.ticker.MultipleLocator(900))
    axes[0].get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes[0].ticklabel_format(axis="y", style="sci", scilimits=(3,3))
    axes[0].set_ylabel(r"$\ln \mathcal{A}_{MC}(\beta)$")

    axes[1].set_ylabel(r"$\Delta \ln \mathcal{A}_{MC}(\beta)$")
    axes[1].set_xticks(xticks)
    axes[1].set_xticklabels(xticklabels)
    axes[1].set_xlim(left=0., right=1.)
    axes[1].set_xlabel(r"inverse temperature $\beta$")

    fig.align_ylabels(axes)
    fig.savefig(OUTPUT, dpi=400)
