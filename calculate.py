# 01.01.2023 -> Sunday
# leap year - 366 days, year - 365 days
# if year % 4 = 0 then year is leap year
from datetime import date
from sys import maxsize


def get_today_date() -> date:
    return date.today()


def determine_day_of_week(date: str) -> str:
    months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    try:
        day, month, year = (int(i)for i in date.split("."))
        if year % 4 == 0:
            months[2] = 29
        if not (2023 <= year and 1 <= month <= 12 and 1 <= day <= months[month]):
            raise ValueError
    except ValueError:
        return "ValueError: " + date

    leap_years = (year - 2000) // 4 - (2023 - 2000) // 4

    count_of_days = day + sum(months[:month]) + (year - 2023) * 365 + leap_years - 1
    return days_of_week[count_of_days % 7]


def determine_month(month: str) -> str:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    return months[int(month) - 1]


def next_date(date: str) -> tuple:
    months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    try:
        day, month, year = (int(i)for i in date.split("."))
        if year % 4 == 0:
            months[2] = 29
        if not (2023 <= year and 1 <= month <= 12 and 1 <= day <= months[month]):
            raise ValueError
    except ValueError:
        return "ValueError: " + date, False

    if day + 1 <= months[month]:
        return str(day + 1).zfill(2) + "." + str(month).zfill(2) + "." + str(year), False
    else:
        return "01" + "." + str(month + 1).zfill(2) + "." + str(year), True


def get_positions(dates: list) -> dict:
    days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    positions = ["" for _ in range(35)]
    i = days_of_week[determine_day_of_week(dates[0])]
    date = dates[0]
    months_positions = ["" for _ in range(5)]
    months_positions[0] = determine_month(date.split(".")[1])

    while date != dates[-1] and i < 34:
        if date in dates:
            positions[i] = date
        i += 1
        date, f = next_date(date)
        if f and i % 7 != 1:
            i = i + 7
        if f:
            months_positions[(i // 7)] = determine_month(date.split(".")[1])

    positions[i] = date
    return {"positions": positions[:i+1], "months_positions": months_positions}


def get_event_id(group_id: str, event_name: str, date1: str) -> int:
    return hash(group_id + event_name + date1) % (maxsize + 1)


def generate_days(date1: str, date2: str = None) -> list:
    date = date1
    resp = list()
    if date2:
        while date != date2:
            resp.append(date)
            date, f = next_date(date)
    else:
        for i in range(35):
            resp.append(date)
            date, f = next_date(date)

    resp.append(date)
    return resp
