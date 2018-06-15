"""Routes and view functions for timer app and API"""

from datetime import datetime, timedelta

from flask import request, jsonify, abort, render_template

from app.timer import ploter
from . import timer
from ..models import Timer_entries, Timer_summary


@timer.route('/v0.1/posttime', methods=["POST"])
def post_time():
    if not request.json or not "work_time" in request.json or not "start_time" in request.json:
        abort(400)

    starttime = request.json["start_time"]
    totaltime = request.json["work_time"]

    starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)

    totaltime_todatetime = datetime.strptime(totaltime, "%H:%M:%S.%f")
    delta = timedelta(hours=totaltime_todatetime.hour, minutes=totaltime_todatetime.minute, seconds=totaltime_todatetime.second)

    Timer_entries.entry_setter(starttime, delta) #Database insert handled by model-specific classmethods

    timer_data_point = {
        "start_time": request.json["start_time"],
        "work_time": request.json["work_time"]
    }

    return jsonify({'timer_data_point': timer_data_point}), 201

@timer.route('/v0.1/gettime', methods=["GET"])
def get_time():

    days_range = request.args.get('days', None, type=int)

    totaltime = timedelta()

    if days_range:
        yesterday = datetime.today() - timedelta(days=days_range)
        all_times = Timer_entries.query.filter(yesterday < Timer_entries.entry_starttime).all()
    else:
        all_times = Timer_entries.query.all()

    for time in all_times:
        totaltime += time.entry_totaltime

    return str(totaltime), 201

@timer.route('/v0.1/runtime_test', methods=["GET", "POST"])
def runtime_test():
    if not request.json or not "test_data" in request.json:
        abort(400)
    else:
        return "", 201

@timer.route('/summary')
def summary():
    user_id = request.args.get('user_id', type=int)
    if user_id:
        summary = Timer_summary.query.filter_by(id=user_id).first_or_404()
        ploter.plot(user_id)
        return render_template("timer_summary.html", summary=summary, chart="chart-{}-30.png".format(user_id))
    else:
        abort(404)


