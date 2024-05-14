"""
Plot histograms of predicted and posteriors over observed prevalences for scenarios
that involve the LNLs I and II. Compare these prevalence predictions for the base-graph
model to the winning-graph model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from lyscripts.plot.utils import Histogram, Posterior, draw
from lyscripts.plot.utils import COLORS as USZ
from tueplots import figsizes, fontsizes

import paths


BASE_GRAPH_INPUT = paths.data / "bg_IandII_prevs.hdf5"
WIN_GRAPH_INPUT = paths.data / "wg_IandII_prevs.hdf5"
OUTPUT = (paths.figures / Path(__file__).name).with_suffix(".png")
NROWS, NCOLS = 2, 2


if __name__ == "__main__":
    plt.rcParams.update(figsizes.icml2022_full(
        nrows=NROWS,
        ncols=NCOLS,
        height_to_width_ratio=0.45,
    ))
    plt.rcParams.update(fontsizes.icml2022())
    fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, sharex="col")


    left_panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        left_panels[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"I/{stage}",
                label="winning graph",
                color=USZ["blue"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"I/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"I/{stage}",
                color=USZ["blue"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"InotII/{stage}",
                label="winning graph",
                color=USZ["green"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"InotII/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"\\\\",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"InotII/{stage}",
                color=USZ["green"],
            ),
        ]

    for stage in ["early", "late"]:
        for content in left_panels[stage]:
            if isinstance(content, Posterior):
                content.kwargs["label"] = f"{content.num_success} / {content.num_total} patients"

    draw(axes[0,0], contents=left_panels["early"], xlims=(0., 16.), hist_kwargs={"nbins": 40})
    h, l = axes[0,0].get_legend_handles_labels()
    legend = axes[0,0].legend(
        h[:3], l[:3],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL I overall",
        title_fontsize="x-small",
    )
    axes[0,0].add_artist(legend)
    legend = axes[0,0].legend(
        h[3:6], l[3:6],
        loc="upper left",
        bbox_to_anchor=(0.15, 0.99),
        title="LNL I without II",
        title_fontsize="x-small",
    )
    axes[0,0].add_artist(legend)
    axes[0,0].set_ylim(bottom=0., top=1.5)
    axes[0,0].set_yticks([0., 0.5, 1.0, 1.5])
    axes[0,0].set_ylabel("density")
    _ax = axes[0,0].secondary_yaxis("left")
    _ax.tick_params(axis="y", left=False, labelleft=False)
    _ax.set_ylabel("early T-cat.", fontweight="bold", labelpad=30)

    draw(axes[1,0], contents=left_panels["late"], xlims=(0., 16.), hist_kwargs={"nbins": 40})
    h, l = axes[1,0].get_legend_handles_labels()
    legend = axes[1,0].legend(
        h[:3], l[:3],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL I overall",
        title_fontsize="x-small",
    )
    axes[1,0].add_artist(legend)
    legend = axes[1,0].legend(
        h[3:6], l[3:6],
        loc="upper left",
        bbox_to_anchor=(0.15, 0.99),
        title="LNL I without II",
        title_fontsize="x-small",
    )
    axes[1,0].add_artist(legend)
    axes[1,0].set_ylabel("density")
    axes[1,0].set_xlabel("prevalence [%]")
    _ax = axes[1,0].secondary_yaxis("left")
    _ax.tick_params(axis="y", left=False, labelleft=False)
    _ax.set_ylabel("early T-cat.", fontweight="bold", labelpad=30)

    fig.align_labels(axes[:,0])


    right_panels = {
        "early": [],
        "late": [],
    }

    for stage in ["early", "late"]:
        right_panels[stage] = [
            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"II/{stage}",
                label="winning graph",
                color=USZ["red"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"II/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"////",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"II/{stage}",
                color=USZ["red"],
            ),

            Histogram.from_hdf5(
                filename=WIN_GRAPH_INPUT,
                dataname=f"IInotI/{stage}",
                label="winning graph",
                color=USZ["orange"],
            ),
            Histogram.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IInotI/{stage}",
                label="base graph",
                histtype="step",
                color="black",
                linewidth=2.,
                hatch=r"\\\\",
            ),
            Posterior.from_hdf5(
                filename=BASE_GRAPH_INPUT,
                dataname=f"IInotI/{stage}",
                color=USZ["orange"],
            ),
        ]

    for stage in ["early", "late"]:
        for content in right_panels[stage]:
            if isinstance(content, Posterior):
                content.kwargs["label"] = f"{content.num_success} / {content.num_total} patients"

    draw(axes[0,1], contents=right_panels["early"], xlims=(45., 100.), hist_kwargs={"nbins": 50})
    axes[0,1].set_ylabel("density")
    axes[0,1].set_yticks([0., 0.1, 0.2, 0.3])
    h, l = axes[0,1].get_legend_handles_labels()
    legend = axes[0,1].legend(
        h[:3], l[:3],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL II overall",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[0,1].add_artist(legend)
    legend = axes[0,1].legend(
        h[3:6], l[3:6],
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        title="LNL II without I",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[0,1].add_artist(legend)
    axes[0,1].set_ylim(bottom=0., top=0.3)

    draw(axes[1,1], contents=right_panels["late"], xlims=(45., 100.), hist_kwargs={"nbins": 50})
    axes[1,1].set_ylabel("density")
    axes[1,1].set_yticks([0., 0.1, 0.2, 0.3])
    axes[1,1].set_xlabel("prevalence [%]")
    h, l = axes[1,1].get_legend_handles_labels()
    legend = axes[1,1].legend(
        h[:3], l[:3],
        loc="upper right",
        bbox_to_anchor=(0.99, 0.99),
        title="LNL II overall",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[1,1].add_artist(legend)
    legend = axes[1,1].legend(
        h[3:6], l[3:6],
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        title="LNL II without I",
        title_fontsize="x-small",
        labelspacing=0.3,
    )
    axes[1,1].add_artist(legend)
    axes[1,1].set_ylim(bottom=0., top=0.3)

    fig.suptitle("Base and winning graph's prevalence predictions", fontweight="bold")
    plt.savefig(OUTPUT, dpi=300)
