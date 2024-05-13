"""
Create a plot that investigates how sensitive the risk predictions are
to the sensitivity & specificity of the diagnostic modality.
"""
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from lymph import Unilateral
from lyscripts.plot.utils import COLORS as USZ
from lyscripts.utils import load_hdf5_samples
from tueplots import figsizes, fontsizes

import paths


SAMPLES_PATH = paths.data / "wg_samples.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
WINNING_GRAPH = {
    ("tumor", "primary"): ["I", "II", "III", "IV", "V", "VII"],
    ("lnl", "I"): ["II"],
    ("lnl", "II"): ["III"],
    ("lnl", "III"): ["IV"],
    ("lnl", "IV"): ["V"],
    ("lnl", "V"): [],
    ("lnl", "VII"): [],
}
PATTERN_OF_INTEREST = {"IV": True}
DIAGNOSIS = {
    "risk": {"I": False, "II": True, "III": True, "IV": False, "V": False, "VII": False}
}
T_STAGE = "late"
NSTEP = 11
MAX_T = 10
TIME_STEPS = np.arange(MAX_T + 1)
CMAP = LinearSegmentedColormap.from_list(
    "usz_cmap", [USZ["blue"], USZ["gray"], USZ["red"]]
)


if __name__ == "__main__":
    model = Unilateral(WINNING_GRAPH)
    samples = load_hdf5_samples(SAMPLES_PATH)

    samples_mean = np.mean(samples, axis=0)
    spread_probs = samples_mean[:-1]
    time_dist_prob = samples_mean[-1]

    model.spread_probs = spread_probs
    model.diag_time_dists[T_STAGE] = sp.stats.binom.pmf(
        TIME_STEPS, MAX_T, time_dist_prob,
    )

    risk_map = np.empty(shape = (NSTEP, NSTEP), dtype=float)

    for i,sens in enumerate(np.linspace(0.5, 1., NSTEP)):
        for j,spec in enumerate(np.linspace(0.5, 1., NSTEP)):
            model.modalities = {"risk": [spec, sens]}
            risk_map[i,j] = model.risk(
                involvement=PATTERN_OF_INTEREST,
                given_diagnoses=DIAGNOSIS,
                t_stage=T_STAGE,
            )

    plt.rcParams.update(figsizes.icml2022_half(
        nrows=1, ncols=1, height_to_width_ratio=1.,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=1, ncols=1)

    image = axes.imshow(
        100 * risk_map,
        interpolation="none",
        aspect="equal",
        origin="lower",
        vmin=0., vmax=14.,
        extent=(47.5, 102.5, 47.5, 102.5),
        cmap=CMAP,
    )
    axes.set_title("LNL IV, given LNL II, III involved", fontweight="bold")

    labels = [f"{100*v:.0f}" for v in np.linspace(0.5, 1., 6)]

    axes.set_yticks(np.linspace(50., 100., 6))
    axes.set_ylabel("sensitivity [%]")

    axes.set_xticks(np.linspace(50., 100., 6))
    axes.set_xlabel("specificity [%]")

    divider = make_axes_locatable(axes)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = plt.colorbar(image, cax=cax)
    cbar.set_ticks(np.linspace(0., 14., 8))
    cbar.set_label("risk [%]")

    plt.savefig(OUTPUT, dpi=300)
