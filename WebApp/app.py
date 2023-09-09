from flask import Flask, render_template, request
from calculate import get_today_date, generate_days, get_positions


app = Flask(__name__)


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

# If I decide server to get response
# @app.post("/create_calendar")
# def create_calendar():
#     print(request.get_json())
#     return make_response({'message': 'Done', 'code': 'SUCCESS'}, 200)


@app.get("/vote")
def vote():
    return render_template("vote.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2003, debug=False)
