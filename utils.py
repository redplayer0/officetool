from datetime import datetime, timedelta

from ortools.linear_solver import pywraplp


def date_fromstr(string):
    return datetime.fromisoformat(string).date()


def str_fromdate(date: datetime):
    return date.strftime("%Y-%m-%d")


def dates_list(s1, s2):
    dates = [s1]

    d = timedelta(days=1)
    start = date_fromstr(s1)
    end = date_fromstr(s2)

    while True:
        if start == end:
            break
        start += d
        dates.append(str_fromdate(start))

    return dates


def dates_dict(dates, dlist):
    date_params = {}
    for d in dates:
        date_params[d] = {}
    for item in dlist:
        cost = 1
        date = item["date"]
        types = item["types"]
        date_params[d]["types"] = types

    return date_params


def get_dates(s1, s2, dlist):
    dates = dates_list(s1, s2)
    return dates_dict(dates, dlist)


def gen_initial_variables(
    model: pywraplp.Solver, dates, people, tasks
) -> dict[tuple[str, str, str], bool]:
    x = {}
    for d, date in dates.items():
        for p, person in people.items():
            for t, task in tasks.items():
                x[d, p, t] = model.BoolVar("")
    return x


def filter_vars(
    vars,
    dates: str | list[str] | tuple[str, str] | None = None,
    names: str | list[str] | None = None,
    tasks: str | list[str] | None = None,
):
    filtered = vars
    if dates:
        if isinstance(dates, str):
            filtered = [t for t in filtered if t[0] == dates]
        elif isinstance(dates, list):
            filtered = [t for t in filtered if t[0] in dates]
        elif isinstance(dates, tuple):
            if len(dates) == 2:
                date_range = dates_list(dates[0], dates[1])
                filtered = [t for t in filtered if t[0] in date_range]
            else:
                raise ValueError(f"A tuple {dates} should have only 2 elements")

    if names:
        if isinstance(names, str):
            filtered = [t for t in filtered if names in t[1]]
        elif isinstance(dates, list):
            filtered = [t for t in filtered if t[1] in names]

    if tasks:
        if isinstance(tasks, str):
            filtered = [t for t in filtered if t[2] == tasks]
        elif isinstance(dates, list):
            filtered = [t for t in filtered if t[2] in tasks]

    return filtered


def roller(l: list, window: int) -> list:
    length = len(l)
    end = length - window + 1
    for i in range(end):
        yield l[i : i + window]


def roller_vars(vars, l: list, window: int) -> list:
    length = len(l)
    end = length - window + 1
    for i in range(end):
        yield [vars[v] for v in l[i : i + window]]
