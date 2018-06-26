"""Routes and view functions for timer app and API"""

from datetime import datetime, timedelta

from flask import request, jsonify, abort, render_template

from app.timer import ploter
from . import timer
from ..models import Timer_entries, Timer_summary


@timer.route('/v0.1/posttime', methods=["POST"])
def post_time():
    if not request.json or not "worktime" in request.json or not "starttime" in request.json:
        abort(400)

    username = request.json["username"]
    starttime = request.json["starttime"]
    totaltime = request.json["worktime"]

    starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")

    totaltime_todatetime = datetime.strptime(totaltime, "%H:%M:%S.%f")
    delta = timedelta(hours=totaltime_todatetime.hour, minutes=totaltime_todatetime.minute, seconds=totaltime_todatetime.second)

    Timer_entries.entry_setter(starttime, delta, username) #Database insert handled by model-specific class methods

    timer_data_point = {
        "success": "true",
        "username": request.json["username"],
        "starttime": request.json["starttime"],
        "worktime": request.json["worktime"]
    }

    return jsonify({'timer_data_point': timer_data_point}), 201

@timer.route('/v0.1/gettime', methods=["GET"])
def get_time():

    days_range = request.args.get('days', None, type=int)
    username = request.args.get('username', "main", type=str)

    totaltime = timedelta()

    if days_range:
        yesterday = datetime.today() - timedelta(days=days_range)
        all_times = Timer_entries.query.filter(yesterday < Timer_entries.starttime).all()
    else:
        all_times = Timer_entries.query.all()

    for time in all_times:
        totaltime += time.totaltime

    return jsonify({"username": username, "totaltime": str(totaltime)}), 200

@timer.route('/v0.1/runtime_test', methods=["GET", "POST"])
def runtime_test():
    "Simple test method for timer script to execute at runtime."
    if not request.json or not "test_data" in request.json:
        abort(400)
    else:
        return "", 201

@timer.route('/summary')
def summary():
    username = request.args.get('username', type=str)
    if username:
        summary = Timer_summary.query.filter_by(username=username).first_or_404()
        ploter.plot(summary.username)
        return render_template("timer_summary.html", summary=summary, chart="chart-{}-30.png".format(username)), 200
    else:
        abort(400)


