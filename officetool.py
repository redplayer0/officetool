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


def get_person_costs(person, dates, plan):
    history = person["history"]
    months = person.get("months", 0)
    costs = {}
    for day in plan:
        ...


if __name__ == "__main__":
    import sys

    target = sys.argv[1]
    # output = sys.argv[2]

    with open(target, "r") as f:
        dt = json.load(f)

    dates = dates_list(dt["plan"]["startDate"], dt["plan"]["endDate"])
    people = people_dict(dt["people"])

    example_costs = get_person_costs(dt["people"][0], dates, dt["plan"])
    pprint(example_costs)
