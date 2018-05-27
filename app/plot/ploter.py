import matplotlib.pyplot as ploter
import matplotlib.dates
import matplotlib.style as mplstyle
from datetime import timedelta, datetime
from ..models import Timer

def plot(days = 30):
    mplstyle.use(['ggplot'])

    days_range = datetime.today() - timedelta(days=days)

    dbcheck = Timer.query.filter(Timer.entry_starttime > days_range).all()

    dates = [matplotlib.dates.date2num(dbentry.entry_starttime.replace(second=0, minute=0, hour=0)) for dbentry in dbcheck]
    times = [dbentry.entry_totaltime.total_seconds() / 60 for dbentry in dbcheck] #seconds -> minutes

    days_x_format = matplotlib.dates.DayLocator(interval=5)
    hours_x_format = matplotlib.dates.DayLocator()
    daysFmt_x_format = matplotlib.dates.DateFormatter('%d-%m')

    fig, ax = ploter.subplots()

    ax.bar(dates, times)
    ax.set(xlabel = "Data", ylabel="Czas pracy [minuty]")

    ax.xaxis.set_major_locator(days_x_format)
    ax.xaxis.set_major_formatter(daysFmt_x_format)
    ax.xaxis.set_minor_locator(hours_x_format)

    ax.grid(True)

    ploter.savefig("nice.png")
