import pandas as pd

from utils import dates_list


def get_people(people):
    p = {}
    for person in people:
        p[person["uuid"]] = person
    return p


def costs_dict(dates, people, plan):
    costs = {}
    for name, person in people.items():
        costs[name] = {}
        costs_dict = costs[name]
        for day in dates:
            ...


def get_person_costs_per_day(history, dates):
    months = history.get("months", 1)
    costs = {}
    for date, params in dates.items():
        cost = 1
        if "types" in params:
            types = params["types"]
            for t in types:
                cost += history.get(t, 0) / months
        else:
            cost += history.get("normal", 0) / months
        costs[date] = cost
    return costs


def get_all_people_costs(people, dates):
    costs = {}
    for name, values in people.items():
        person_costs = get_person_costs_per_day(values["history"], dates)
        for date, cost in person_costs.items():
            for task in values["possibleTasks"]:
                costs[date, name, task] = cost
    return costs


def adjust_costs(people, costs, pref_modifiers):
    for name, person in people.items():
        for p in person.get("parameters", {}).get("preferences", []):
            start = p.get("date", None)
            end = p.get("toDate", None)
            opt = p.get("option", None)
            if opt:
                coef = pref_modifiers[opt]
            for task in person["possibleTasks"]:
                if end:
                    for date in dates_list(start, end):
                        costs[date, name, task] *= coef


def get_tasks(tasks):
    t = {}
    for task in tasks:
        t[task.pop("taskName")] = task
    return t


def get_dataframes(xlsx, sheets):
    dts = {}
    for sheet in sheets:
        dts[sheet] = (
            pd.read_excel(
                xlsx,
                sheet_name=sheet,
                parse_dates=True,
                date_format="%Y-%m-%d",
            )
            .fillna("")
            .to_dict("index")
        )
    return dts


def get_preferences(dt):
    prefs = {}
    for row, data in dt.items():
        uuid = data.pop("uuid")
        prefs[uuid] = {k: v for k, v in data.items()}
    return prefs
