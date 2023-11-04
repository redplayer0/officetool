import json
from pprint import pprint

from collect_data import get_all_people_costs, get_people, get_tasks
from utils import get_dates

if __name__ == "__main__":
    import sys

    target = sys.argv[1]
    # output = sys.argv[2]

    with open(target, "r") as f:
        dt = json.load(f)

    plan = dt["plan"]
    dates = get_dates(plan["startDate"], plan["endDate"], plan["datesList"])
    people = get_people(dt["people"])
    tasks = get_tasks(dt["tasks"])
    costs = get_all_people_costs(people, dates)

    x = {}
    for d, date in dates.items():
        for p, person in people.items():
            for t, task in tasks.items():
                x[d, p, t] = 1

    pprint(plan)
