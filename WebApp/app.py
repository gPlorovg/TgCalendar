from flask import Flask, render_template

app = Flask(__name__)


@app.get("/config_calendar")
def config_calendar_page():
    return render_template("config_calendar.html")


@app.get("/vote")
def vote_page():
    return render_template("vote.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567, debug=False)
