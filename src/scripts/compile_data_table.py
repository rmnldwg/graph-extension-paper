"""
Fetch the current patient and involvement numbers from LyProX and put
them via a Jinja template into a LaTeX table that can be displayed in
the paper.
"""
import re

from jinja2 import Environment, FileSystemLoader
import requests
from bs4 import BeautifulSoup
import yaml

import paths


BASE_URL = "https://lyprox.org/dashboard"
URL_PARAMS_PATH = paths.scripts / "default_dashboard_params.yaml"
TSTAGE_PARAMS = {
    "early": {"t_stage__in": 1, "t_stage__in": 2},
    "late" : {"t_stage__in": 3, "t_stage__in": 4},
}
SCENARIO_PARAMS = {
    "I": {"ipsi_I": 1},
}
TEMPLATE_NAME = "data_table.temp"
OUTPUT = paths.output / "data_table.tex"


with open(URL_PARAMS_PATH, mode="r", encoding="utf-8") as url_params_file:
    default_url_params = yaml.safe_load(url_params_file)

for stage, stage_params in TSTAGE_PARAMS.items():
    for scenario, scenario_params in SCENARIO_PARAMS.items():
        url_params = default_url_params.copy()
        url_params.update(stage_params)
        url_params.update(scenario_params)

        response = requests.get(url=BASE_URL, params=url_params, timeout=1000)
        if not response.ok:
            raise ConnectionError("Request failed.")
        soup = BeautifulSoup(response.text, "html.parser")
        button_text = soup.html.find(
            "button",
            class_="button is-medium is-warning is-light is-outlined"
        ).span.text
        number = re.match(r"[0-9]{1,3}", button_text)


response = requests.get(
    url=BASE_URL,
    params=url_params,
)


environment = Environment(
    loader=FileSystemLoader(paths.scripts)
)
table_template = environment.get_template(TEMPLATE_NAME)
context = {}


with open(BASE_GRAPH_INPUT, mode="r") as bg_file:
    bg_metrics = json.load(bg_file)

for key,val in bg_metrics.items():
    context[f"bg_{key}"] = val


with open(OUTPUT, mode="w") as table_file:
    table_file.write(table_template.render(**context))
