"""
Fetch the current patient and involvement numbers from LyProX and put
them via a Jinja template into a LaTeX table that can be displayed in
the paper.
"""
import re

from jinja2 import Environment, FileSystemLoader, exceptions
import yaml
from lyscripts.plot.utils import Posterior

import paths


TEMPLATE_NAME = "data_table.temp"
OUTPUT = paths.output / "data_table.tex"
REGEX_PATTERN = r"(^[wb]g_[IV]{1,3}and[IV]{1,3})_.+\.yaml$"


scenarios = {"early": [], "late": []}
yaml_file_paths = paths.scripts.glob("*.yaml")
for yaml_file_path in yaml_file_paths:
    regex_match = re.match(REGEX_PATTERN, yaml_file_path.name)

    if regex_match is None:
        continue

    with open(yaml_file_path, mode="r", encoding="utf-8") as yaml_file:
        yaml_params = yaml.safe_load(yaml_file)

    hdf_file_path = paths.data / f"{regex_match[1]}_prevs.hdf5"
    for scenario in yaml_params["prevalences"]:
        posterior = Posterior.from_hdf5(
            filename=hdf_file_path,
            dataname=scenario["name"],
        )
        scenario.update({
            "num_success": posterior.num_success,
            "num_total": posterior.num_total,
        })
        scenario["pattern"] = scenario["pattern"]["ipsi"]
        scenarios[scenario["t_stage"]].append(scenario)


for early_sc, late_sc in zip(scenarios["early"], scenarios["late"]):
    if early_sc["pattern"] != late_sc["pattern"]:
        raise RuntimeError("Early and late scenarios don't match.")

if len(scenarios["early"]) != len(scenarios["late"]):
    raise RuntimeError("Not the same number of early and late scenarios")


def get_lnl(value_dict, lnl):
    try:
        value = value_dict[lnl]
    except KeyError:
        return "?"
    if value:
        return r"{\color{red} \CIRCLE}"
    return r"{\color{green} \CIRCLE}"

def prev(value):
    percent = int(100. * value["num_success"] / value["num_total"])
    return f"{value['num_success']}/{value['num_total']} ({percent:d}\%)"


environment = Environment(
    loader=FileSystemLoader(paths.scripts)
)
environment.filters["get_lnl"] = get_lnl
environment.filters["prev"] = prev
environment.filters["zip"] = zip
table_template = environment.get_template(TEMPLATE_NAME)
context = {"scenarios": scenarios}


with open(OUTPUT, mode="w", encoding="utf-8") as table_file:
    table_file.write(table_template.render(**context))
