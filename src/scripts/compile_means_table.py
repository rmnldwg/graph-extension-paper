"""
Write all mean parameter samples to a markdown table.
"""
from jinja2 import Environment, FileSystemLoader
from emcee.backends import HDFBackend

import paths


INPUT = paths.data / "wg_samples.hdf5"
TEMPLATE_NAME = "means_table.temp"
OUTPUT = paths.output
NAMES = [
    r"b_\text{I}",
    r"b_\text{II}",
    r"b_\text{III}",
    r"b_\text{IV}",
    r"b_\text{V}",
    r"b_\text{VII}",
    r"t_{\text{I} \rightarrow {II}}",
    r"t_{\text{II} \rightarrow {III}}",
    r"t_{\text{III} \rightarrow {IV}}",
    r"t_{\text{IV} \rightarrow {V}}",
    r"p_\text{late}",
]


if __name__ == "__main__":
    # open samples
    backend = HDFBackend(paths.data / INPUT, read_only=True)
    samples = backend.get_chain(flat=True)
    means = samples.mean(axis=0)
    stddevs = samples.std(axis=0)

    lines = []
    for name, mean, std in zip(NAMES, means, stddevs):
        lines.append({
            "name": name,
            "mean": 100 * mean,
            "std": 100 * std,
        })

    environment = Environment(loader=FileSystemLoader(paths.scripts))
    template = environment.get_template(TEMPLATE_NAME)

    with open(OUTPUT / "means_table.tex", "w") as f:
        f.write(template.render(lines=lines))
