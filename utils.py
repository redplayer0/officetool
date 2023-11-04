from datetime import datetime, timedelta


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
