from flask import Flask, render_template, request
from calculate import get_today_date


app = Flask(__name__)


@app.get("/pre_config_calendar")
def pre_config_calendar():
    return render_template("pre_config_calendar.html", today_date=get_today_date())


@app.get("/config_calendar")
def config_calendar():
    event_name = request.args.get("event_name")
    start_date = request.args.get("start_date")
    return render_template("config_calendar.html", event_name=event_name, start_date=start_date)


@app.get("/vote")
def vote():
    return render_template("vote.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=False)
