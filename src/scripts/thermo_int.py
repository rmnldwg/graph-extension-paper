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
POWER = 5


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_half())
    plt.rcParams.update(fontsizes.icml2022())
    plt.rcParams.update({"text.usetex": False})
    fig, axes = plt.subplots()

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

    errors = accuracies.copy().drop(
        columns=["lose graph", "win graph"]
    ).rename(
        columns={"std_": "lose graph", "std": "win graph"}
    )
    errors["β"] = errors["β"] ** (1./POWER)
    accuracies = accuracies.drop(columns=["std_", "std"])
    accuracies["β"] = accuracies["β"] ** (1./POWER)

    accuracies.plot(
        x="β",
        y=["lose graph", "win graph"],
        ax=axes,
        color=[USZ["red"], USZ["blue"]],
        label=["remove II → III & III → IV", "add I → II & IV → V"],
    )

    xticks = np.linspace(0., 1., 7)
    xticklabels = [f"{x**POWER:.2g}" for x in xticks]
    axes.set_xticks(xticks)
    axes.set_xticklabels(xticklabels)
    axes.set_xlim(left=0., right=1.)
    axes.set_xlabel(r"inverse temperature $\beta$")
    axes.set_yscale("symlog",)
    axes.get_yaxis().set_major_locator(matplotlib.ticker.MultipleLocator(800))
    axes.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axes.ticklabel_format(axis="y", style="sci", scilimits=(2,2))
    axes.set_ylabel(r"$\ln \mathcal{A}_{MC}(\beta)$")

    fig.savefig(OUTPUT, dpi=400)
