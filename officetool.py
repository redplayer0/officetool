import json
from pprint import pprint

import pandas as pd
from ortools.linear_solver import pywraplp

from collect_data import (
    adjust_costs,
    get_all_people_costs,
    get_dataframes,
    get_people,
    get_tasks,
    get_preferences,
)


from utils import get_dates


def json_draft(file):
    with open(target, "r") as f:
        dt = json.load(f)

    pref_modifiers = dt["options"]["peoplePreferences"]
    plan = dt["plan"]
    dates = get_dates(plan["startDate"], plan["endDate"], plan["datesList"])
    people = get_people(dt["people"])
    tasks = get_tasks(dt["tasks"])
    costs = get_all_people_costs(people, dates)
    adjust_costs(people, costs, pref_modifiers)

    # added typing for better lsp support
    model: pywraplp.Solver = pywraplp.Solver.CreateSolver("SCIP")
    # vars = gen_initial_variables(model, dates, people, tasks)
    varnames = list(costs.keys())
    vars = {}
    for c in costs:
        vars[c] = model.BoolVar("")

    # test = filter_vars(
    #     vars, dates=("2023-11-03", "2023-11-06"), names="L", tasks="ΕΕΑΣ"
    # )

    # for window in roller_vars(vars, test, 2):
    #     pprint(window)


def xlsx_draft(file):
    xlsx = pd.ExcelFile("draft.xlsx")
    sheets = xlsx.sheet_names
    dts = get_dataframes(xlsx, sheets)

    preferences = get_preferences(dts["preferences"])

    dt = {}
    dt["plan"] = []
    for v in dts["plan"].values():
        ...


if __name__ == "__main__":
    import sys

    target = sys.argv[1]
    # output = sys.argv[2]

    if target.endswith(".json"):
        json_draft(target)
    elif target.endswith(".xlsx"):
        xlsx_draft(target)

    xlsx_draft("draft.xlsx")
