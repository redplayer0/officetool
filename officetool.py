import json
from datetime import datetime, timedelta
from pprint import pprint

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


def people_dict(people):
    p = {}
    for person in people:
        fullname = f"{person['lastName']} {person['firstName']} του {person.get('fatherName', '')}"
        p[fullname] = person

    return p


def costs_dict(dates, people, plan):
    costs = {}
    for name, person in people.items():
        costs[name] = {}
        costs_dict = costs[name]
        for day in dates:
            ...


def get_person_costs(history, date_params):
    months = history.get("months", 1)
    costs = {}
    for date, params in date_params.items():
        cost = 1
        if "types" in params:
            types = params["types"]
            for t in types:
                cost += history.get(t, 0) / months
        else:
            cost += history.get("normal", 0) / months
        costs[date] = cost
    return costs


def get_all_people_costs(people, date_params):
    return {
        name: get_person_costs(values.get("history"), date_params)
        for name, values in people.items()
    }


if __name__ == "__main__":
    import sys

    target = sys.argv[1]
    # output = sys.argv[2]

    with open(target, "r") as f:
        dt = json.load(f)

    dates = dates_list(dt["plan"]["startDate"], dt["plan"]["endDate"])
    date_params = dates_dict(dates, dt["plan"]["datesList"])
    people = people_dict(dt["people"])
    print(people)

    example_costs = get_all_people_costs(people, date_params)
    pprint(example_costs)
