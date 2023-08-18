"""
Write all mean parameter samples to a markdown table.
"""
import pandas as pd
from emcee.backends import HDFBackend

import paths


INPUT = paths.data / "wg_samples.hdf5"
OUTPUT = paths.output
NAMES = [
    r"b_\text{I}",
    r"b_\text{II}",
    r"b_\text{III}",
    r"b_\text{IV}",
    r"b_\text{V}",
    r"b_\text{VII}",
    r"t_{\text{II} \rightarrow {I}}",
    r"t_{\text{II} \rightarrow {III}}",
    r"t_{\text{II} \rightarrow {V}}",
    r"t_{\text{III} \rightarrow {IV}}",
    r"t_{\text{III} \rightarrow {V}}",
    r"p_\text{late}",
]


if __name__ == "__main__":
    # open samples
    backend = HDFBackend(paths.data / INPUT, read_only=True)
    samples = backend.get_chain(flat=True)
    means = samples.mean(axis=0)
    stddevs = samples.std(axis=0)

    means_dict = {
        f"${name}$": [f"{100 * mean:.2f} \%", f"$\pm$ {100 * std:.2f} \%"]
        for name, mean, std in zip(NAMES, means, stddevs)
    }
    df = pd.DataFrame.from_dict(means_dict, orient="index", columns=["mean", "std. dev."])
    latex_table = df.to_latex(column_format="lrr")

    with open(OUTPUT / "wg_means.tex", "w") as f:
        f.write(latex_table)
