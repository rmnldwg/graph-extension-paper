"""
Plot histograms of predicted and posteriors over observed prevalences for scenarios
that involve the LNLs III, IV, and V. Compare these prevalence predictions for the
base-graph model to the winning-graph model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from lyscripts.plot.utils import Histogram, Posterior, draw
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 2, 2


def add_row_label(ax, label, pad=30):
    _ax = ax.secondary_yaxis("left")
    _ax.tick_params(axis="y", left=False, labelleft=False)
    _ax.set_ylabel(label, fontweight="bold", labelpad=pad)


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.45,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, sharex="col")

    # prevalences of LNLs IV and V
    BASE_GRAPH_INPUT = paths.data / "bg_IVandV_prevs.hdf5"
    WIN_GRAPH_INPUT = paths.data / "wg_IVandV_prevs.hdf5"

    panels_IVandV = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        panels_IVandV[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"IVandV/{stage}",
                label="winning graph",
                color=USZ["orange"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IVandV/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"\\\\",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IVandV/{stage}",
                color=USZ["orange"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"VnotIV/{stage}",
                label="winning graph",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIV/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIV/{stage}",
                color=USZ["blue"],
            ),
        ]

    for stage in ["early", "late"]:
        for content in panels_IVandV[stage]:
            if isinstance(content, Posterior):
                content.kwargs["label"] = f"{content.num_success} / {content.num_total} patients"

    # prevalences of III and V
    BASE_GRAPH_INPUT = paths.data / "bg_IIIandV_prevs.hdf5"
    WIN_GRAPH_INPUT = paths.data / "wg_IIIandV_prevs.hdf5"

    panels_IIIandV = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        panels_IIIandV[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"IIIandV/{stage}",
                label="winning graph",
                color=USZ["red"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IIIandV/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"\\\\",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IIIandV/{stage}",
                color=USZ["red"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"VnotIII/{stage}",
                label="winning graph",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIII/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"VnotIII/{stage}",
                color=USZ["green"],
            ),
        ]

    for stage in ["early", "late"]:
        for content in panels_IIIandV[stage]:
            if isinstance(content, Posterior):
                content.kwargs["label"] = f"{content.num_success} / {content.num_total} patients"

    draw(axes[0,0], contents=panels_IIIandV["early"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    axes[0,0].set_ylim(bottom=0., top=1.2)
    axes[0,0].set_ylabel("density")
    add_row_label(axes[0,0], label="early T-cat.")
    h, l = axes[0,0].get_legend_handles_labels()
    legend = axes[0,0].legend(
        h[:3], l[:3],
        loc="upper left",
        bbox_to_anchor=(0.4, 0.99),
        title="LNL III and V",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[0,0].add_artist(legend)
    legend = axes[0,0].legend(
        h[3:], l[3:],
        loc="lower right",
        bbox_to_anchor=(0.99, 0.01),
        title="LNL V without III",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[0,0].add_artist(legend)

    draw(axes[1,0], contents=panels_IIIandV["late"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    axes[1,0].set_ylim(bottom=0., top=1.0)
    axes[1,0].set_ylabel("density")
    axes[1,0].set_xlabel("prevalence [%]")
    add_row_label(axes[1,0], label="late T-cat.")
    h, l = axes[1,0].get_legend_handles_labels()
    legend = axes[1,0].legend(
        h[:3], l[:3],
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        title="LNL III and V",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[1,0].add_artist(legend)
    legend = axes[1,0].legend(
        h[3:], l[3:],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL V without III",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[1,0].add_artist(legend)

    draw(axes[0,1], contents=panels_IVandV["early"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    axes[0,1].set_ylabel("density")
    h, l = axes[0,1].get_legend_handles_labels()
    legend = axes[0,1].legend(
        h[:3], l[:3],
        loc="upper left",
        bbox_to_anchor=(0.12, 0.99),
        title="LNL IV and V",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[0,1].add_artist(legend)
    legend = axes[0,1].legend(
        h[3:], l[3:],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL V without IV",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[0,1].add_artist(legend)

    draw(axes[1,1], contents=panels_IVandV["late"], xlims=(0., 12.), hist_kwargs={"nbins": 40})
    axes[1,1].set_ylabel("density")
    axes[1,1].set_yticks([0., 0.5, 1.0, 1.5])
    axes[1,1].set_xlabel("prevalence [%]")
    h, l = axes[1,1].get_legend_handles_labels()
    legend = axes[1,1].legend(
        h[:3], l[:3],
        loc="upper left",
        bbox_to_anchor=(0.15, 0.99),
        title="LNL IV and V",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[1,1].add_artist(legend)
    legend = axes[1,1].legend(
        h[3:], l[3:],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL V without IV",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[1,1].add_artist(legend)

    fig.align_ylabels(axes)
    fig.suptitle("Base and winning graph's prevalence predictions", fontweight="bold")
    plt.savefig(OUTPUT, dpi=300)
