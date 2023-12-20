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


def get_lnl_label(match):
    if match[2]:
        filler = "without" if match[2] == "not" else "and"
        return f"LNL {match[1]} {filler} {match[3]}"

    return f"LNL {match[1]} overall"


def draw_early_late_panels(panels, lnl, xlims, ylims=None, idx=0):
    early_ax = plt.subplot(NROWS, NCOLS, idx * 2 + 1)
    late_ax = plt.subplot(NROWS, NCOLS, idx * 2 + 2, sharex=early_ax)

    draw(early_ax, contents=panels[lnl]["early"], xlims=xlims, hist_kwargs={"nbins": 80})
    draw(late_ax, contents=panels[lnl]["late"], xlims=xlims, hist_kwargs={"nbins": 80})

    if ylims:
        early_ax.set_ylim(ylims)

    early_ax.get_xaxis().set_visible(False)
    early_ax.set_yticks([])
    early_ax.set_ylabel("early T-cat.", fontweight="bold")
    early_ax.legend(labelspacing=0.3)

    if ylims:
        late_ax.set_ylim(ylims)

    late_ax.set_yticks([])
    late_ax.set_xlabel("prevalence [%]")
    late_ax.set_ylabel("late T-cat.", fontweight="bold")
    late_ax.legend(labelspacing=0.3)


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.2,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig = plt.figure()

    panels = {lnl: {"early": [], "late": []} for lnl in ["II", "III", "IV"]}
    colors = {
        lnl: {
            "early": cycle(COLORS.values()),
            "late": cycle(COLORS.values()),
        } for lnl in ["II", "III", "IV"]
    }
    for lnl_combo in LNLS_COMBOS:
        lnl_combo = "".join(lnl_combo)
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
                color = next(colors[lnl_block][stage])
                _histo.kwargs["color"] = color
                _post.kwargs["color"] = color
                panels[lnl_block][stage].append(_histo)
                panels[lnl_block][stage].append(_post)

            except KeyError as key_err:
                pass

    draw_early_late_panels(panels, "II", xlims=(20., 85.), idx=0)
    draw_early_late_panels(panels, "III", xlims=(0., 45.), idx=1)
    draw_early_late_panels(panels, "IV", xlims=(0., 18.), ylims=(0., 0.9), idx=2)

    plt.savefig(OUTPUT, dpi=300)
