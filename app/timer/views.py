"""Routes and view functions for timer app and API"""

from flask import request, jsonify, abort, render_template
from datetime import datetime, timedelta
from . import timer
from .. import db
from ..models import Timer


@timer.route('/v0.1/posttime', methods=["POST"])
def post_time():
    if not request.json or not "work_time" in request.json or not "start_time" in request.json:
        abort(400)

    starttime = request.json["start_time"]
    totaltime = request.json["work_time"]

    starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)

    totaltime_todatetime = datetime.strptime(totaltime, "%H:%M:%S.%f")
    delta = timedelta(hours=totaltime_todatetime.hour, minutes=totaltime_todatetime.minute, seconds=totaltime_todatetime.second)

    starttimedb = Timer(entry_starttime=starttime, entry_totaltime = delta)

    db.session.add(starttimedb)

    timer_data_point = {
        "start_time": request.json["start_time"],
        "work_time": request.json["work_time"]
    }

    return jsonify({'timer_data_point': timer_data_point}), 201

@timer.route('/v0.1/gettime', methods=["GET"])
def get_time():

    totaltime = timedelta()

    all_times = Timer.query.all()

    for time in all_times:
        totaltime += time.entry_totaltime

    return str(totaltime)

@timer.route('/v0.1/runtime_test', methods=["GET", "POST"])
def runtime_test():
    if not request.json or not "test_data" in request.json:
        abort(400)
    else:
        return "", 201