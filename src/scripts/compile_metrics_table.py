"""
Populate a Jinja2 LaTeX table template with the metrics from the experiment runs.
"""
import json
from jinja2 import Environment, FileSystemLoader

import paths


BASE_GRAPH_INPUT = paths.data / "bg_metrics.json"
WIN_GRAPH_INPUT = paths.data / "wg_metrics.json"
TEMPLATE_NAME = "results_table.temp"
OUTPUT = paths.output / "results_table.tex"


if __name__ == "__main__":
    environment = Environment(
        loader=FileSystemLoader(paths.scripts)
    )
    table_template = environment.get_template(TEMPLATE_NAME)
    context = {}


    with open(BASE_GRAPH_INPUT, mode="r", encoding="utf-8") as bg_file:
        bg_metrics = json.load(bg_file)

    for key,val in bg_metrics.items():
        context[f"bg_{key}"] = val


    with open(WIN_GRAPH_INPUT, mode="r", encoding="utf-8") as wg_file:
        wg_metrics = json.load(wg_file)

    for key,val in wg_metrics.items():
        context[f"wg_{key}"] = val


    with open(OUTPUT, mode="w", encoding="utf-8") as table_file:
        table_file.write(table_template.render(**context))
