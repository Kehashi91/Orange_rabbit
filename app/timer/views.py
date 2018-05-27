"""Routes and view functions for timer app and API"""

from flask import request, jsonify, abort, render_template
from datetime import datetime, timedelta, date
from sqlalchemy import extract
from . import timer
from .. import db
from ..models import Timer
from ..plot import ploter


@timer.route('/v0.1/posttime', methods=["POST"])
def post_time():
    if not request.json or not "work_time" in request.json or not "start_time" in request.json:
        abort(400)

    starttime = request.json["start_time"]
    totaltime = request.json["work_time"]

    starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)

    totaltime_todatetime = datetime.strptime(totaltime, "%H:%M:%S.%f")
    delta = timedelta(hours=totaltime_todatetime.hour, minutes=totaltime_todatetime.minute, seconds=totaltime_todatetime.second)

    Timer.entry_starttime_setter(starttime, delta)

    timer_data_point = {
        "start_time": request.json["start_time"],
        "work_time": request.json["work_time"]
    }

    return jsonify({'timer_data_point': timer_data_point}), 201

@timer.route('/v0.1/gettime', methods=["GET"])
def get_time():

    totaltime = timedelta()
    yesterday = datetime.today() - timedelta(days=1)


    all_times = Timer.query.filter(yesterday < Timer.entry_starttime).all()

    for time in all_times:
        totaltime += time.entry_totaltime

    rv = {}
    for time in all_times:
        daily_total = timedelta()



    return str(totaltime)

@timer.route('/v0.1/getgraph', methods=["GET"])
def get_graph():
    ploter.plot()
    return "yiis", 201



@timer.route('/v0.1/runtime_test', methods=["GET", "POST"])
def runtime_test():
    if not request.json or not "test_data" in request.json:
        abort(400)
    else:
        return "", 201


"""
    dbcheck = Timer.query.filter(extract('day', Timer.entry_starttime) == starttime.day).first()

    if dbcheck:
        dbentrytime = dbcheck.entry_totaltime + delta
        dbcheck.entry_totaltime = dbentrytime
    else:
        starttimedb = Timer(entry_starttime=starttime, entry_totaltime=delta)
        db.session.add(starttimedb)

"""