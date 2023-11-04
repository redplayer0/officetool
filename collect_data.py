def get_people(people):
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


def get_tasks(tasks):
    t = {}
    for task in tasks:
        t[task.pop("taskName")] = task
    return t
