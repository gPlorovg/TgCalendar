from os import getenv
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from calculate import get_today_date, generate_days, get_positions
from db_manage import DataBase

app = Flask(__name__)

load_dotenv()
HOST = getenv("HOST")
USER = getenv("USER")
DB_PASSWORD = getenv("DB_PASSWORD")
db = DataBase("TgCalendar", USER, HOST, DB_PASSWORD)

@app.get("/pre_config_calendar")
def pre_config_calendar():
    return render_template("pre_config_calendar.html", today_date=get_today_date())


@app.get("/config_calendar")
def config_calendar():
    return render_template("config_calendar.html")


@app.get("/calendar_grid")
def calendar_grid():
    date1 = request.args.get("start_date")
    date1 = ".".join(date1.split("-")[::-1])
    return get_positions(generate_days(date1))


@app.get("/vote")
def vote():
    event_id = request.args.get("e_id")
    return render_template("vote.html", event_id=event_id)


@app.get("/calendar_data")
def calendar_data():
    event_id = int(request.args.get("e_id"))
    dates, event_name, mark_positions = db.read_calendar(event_id)
    resp = get_positions(dates)
    resp["mark_positions"] = mark_positions
    resp["event_name"] = event_name
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2003, debug=False)
