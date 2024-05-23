"""
Plot histograms of predicted and posteriors over observed prevalences for basic
scenarios involving the LNLs II, III and IV. This is to show that the base graph is
already capable of capturing the frequency of these involvement, as well as their
correlations.
"""
from pathlib import Path
from itertools import cycle, product
import re

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw, COLORS
from tueplots import figsizes, fontsizes

import paths


INPUT = paths.data / "bg_core_prevs.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 6, 1
LNLS_COMBOS = list(product(["II", "III", "IV"], ["and", "not"], ["II", "III", "IV"]))
LNLS_COMBOS = [*LNLS_COMBOS, "II", "III", "IV"]
COMBOS_TO_SKIP = ["IVandII"]


def get_lnl_label(match):
    if match[2]:
        filler = "without" if match[2] == "not" else "and"
        return f"LNL {match[1]} {filler} {match[3]}"

    return f"LNL {match[1]} overall"


def get_color(match) -> str:
    if match[0] == "IVnotII":
        return "black"

    if match[2] is None:
        return COLORS["red"]

    if match[2] == "and":
        return COLORS["blue"]

    if match[2] == "not":
        if (
            (match[1] == "II" and match[3] == "III")
            or (match[1] == "III" and match[3] == "IV")
        ):
            return COLORS["orange"]

    return COLORS["green"]


def draw_early_late_panels(panels, lnl, xlims, ylims=None, idx=0):
    early_ax = plt.subplot(NROWS, NCOLS, idx * 2 + 1)
    late_ax = plt.subplot(NROWS, NCOLS, idx * 2 + 2, sharex=early_ax)

    draw(
        early_ax,
        contents=panels[lnl]["early"],
        xlims=xlims,
        hist_kwargs={"nbins": 80, "zorder": 3},
        plot_kwargs={"zorder": 3.1},
    )
    draw(
        late_ax,
        contents=panels[lnl]["late"],
        xlims=xlims,
        hist_kwargs={"nbins": 80, "zorder": 3},
        plot_kwargs={"zorder": 3.1},
    )

    if ylims:
        early_ax.set_ylim(ylims)

    early_ax.tick_params(axis="x", bottom=False, labelbottom=False)
    early_ax.set_ylabel("density")
    _ax = early_ax.secondary_yaxis("left")
    _ax.set_ylabel("early T-cat.", fontweight="bold", labelpad=15)
    _ax.tick_params(axis="y", right=False, labelright=False)

    if ylims:
        late_ax.set_ylim(ylims)

    late_ax.set_xlabel("prevalence [%]")
    late_ax.set_ylabel("density")
    _ax = late_ax.secondary_yaxis("left")
    _ax.set_ylabel("late T-cat.", fontweight="bold", labelpad=15)
    _ax.tick_params(axis="y", right=False, labelright=False)

    return early_ax, late_ax


def create_legends(ax, positions):
    num = len(positions)
    handles, labels = ax.get_legend_handles_labels()

    for i in range(num):
        legend = ax.legend(
            handles[i * 2 : (i+1) * 2],
            labels[i * 2 : (i+1) * 2],
            loc=positions[i],
        )
        ax.add_artist(legend)


def main():
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.2,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig = plt.figure()

    panels = {lnl: {"early": [], "late": []} for lnl in ["II", "III", "IV"]}
    for lnl_combo in LNLS_COMBOS:
        lnl_combo = "".join(lnl_combo)

        if lnl_combo in COMBOS_TO_SKIP:
            continue

        match = re.match(r"([IV]{2,3})(and|not)?([IV]{2,3})?", lnl_combo)
        lnl_block = match[1]
        for stage in ["early", "late"]:
            try:
                _histo = Histogram.from_hdf5(
                    filename=INPUT,
                    dataname=f"{lnl_combo}/{stage}",
                    label=get_lnl_label(match),
                )
                _post = Posterior.from_hdf5(
                    filename=INPUT,
                    dataname=f"{lnl_combo}/{stage}",
                )
                color = get_color(match)
                _histo.kwargs["color"] = color
                _post.kwargs["color"] = color
                _post.kwargs["label"] = f"{_post.num_success} of {_post.num_total} patients"
                panels[lnl_block][stage].append(_histo)
                panels[lnl_block][stage].append(_post)

            except KeyError:
                pass

    early_ax, late_ax = draw_early_late_panels(
        panels, "II",
        xlims=(20., 85.),
        ylims=(0., 0.3),
        idx=0,
    )
    early_ax.set_title(
        "Observed vs predicted prevalences related to LNL II",
        fontweight="bold",
    )
    create_legends(early_ax, positions=[(0.1, 0.7), (0.46, 0.7), (0.81, 0.7),])
    create_legends(late_ax, positions=[(0.02, 0.7), (0.46, 0.7), (0.68, 0.7),])

    early_ax, late_ax = draw_early_late_panels(panels, "III", xlims=(0., 45.), idx=1)
    early_ax.set_title(
        "Observed vs predicted prevalences related to LNL III",
        fontweight="bold",
    )
    create_legends(early_ax, positions=[(0.2, 0.4), (0.18, 0.7), (0.42, 0.7), (0.7, 0.4),])
    create_legends(late_ax, positions=[(0.25, 0.4), (0.12, 0.7), (0.52, 0.7), (0.73, 0.7),])

    early_ax, late_ax = draw_early_late_panels(panels, "IV", xlims=(0., 16.), idx=2)
    early_ax.set_title(
        "Observed vs predicted prevalences related to LNL IV",
        fontweight="bold",
    )
    create_legends(early_ax, positions=[(0.12, 0.7), (0.2, 0.4), (0.4, 0.7),])
    create_legends(late_ax, positions=[(0.12, 0.7), (0.2, 0.4), (0.65, 0.7),])

    plt.savefig(OUTPUT, dpi=300)


if __name__ == "__main__":
    main()
