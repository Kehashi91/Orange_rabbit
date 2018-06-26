"""Database models and definitions."""

from . import db
from datetime import datetime, date, timedelta

from sqlalchemy import extract
from sqlalchemy.orm import validates



#association table for many-to-many relationship for tags
metatags = db.Table('metatags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = "post"

    post_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_body = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    time_added = db.Column(db.Date, nullable=False, default=date.today())
    tags = db.relationship('Tags', secondary=metatags, lazy='subquery',
        backref=db.backref('Post', lazy=True))
    post_type = db.Column(db.Text, nullable=False)

    @validates('post_type')
    def validate_post_type(self, key, post_type):
        """Although it could be boolean value since we have only 2 values, i do not rule out adding diffrent post types
        in the future, so i build a custom validator."""
        post_types_reference = {'project', 'blogpost'}
        if post_type in post_types_reference:
            return post_type
        else:
            raise ValueError("Post type must be: {!r}".format(post_types_reference))

    def __repr__(self):
        return '<portfolioprojects/posts {!r}, description {!r}. time_added {!r}>'.format(
            self.name, self.description, self.time_added)


class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)


    def __repr__(self):
        return '<tag {!r}>'.format(self.name)

class Timer_entries(db.Model):
    __tablename__ = 'timer_entries'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Integer, db.ForeignKey('timer_summary.id'), nullable=False)
    starttime = db.Column(db.DateTime, nullable=False)
    totaltime = db.Column(db.Interval, nullable=False)

    @classmethod
    def entry_setter(cls, starttime, totaltime, username):
        """This function verifies if we have existing entry for current day, if yes, it merely updates it, otherwise
        it creates a new entry. It calls a Timer_summary.new_entry_update specific function to further propagate 
        the update. These functions are kept separate as the manipulate models that coresponds to them."""

        dbcheck = Timer_entries.query.filter(extract('day', Timer_entries.starttime) == starttime.day).first()
        username_to_pass = Timer_summary.query.filter_by(username=username).first()

        if dbcheck:
            dbentrytime = dbcheck.totaltime + totaltime
            dbcheck.totaltime = dbentrytime
        else:
            starttimedb = Timer_entries(starttime=starttime, totaltime=totaltime, username=username_to_pass.id)
            db.session.add(starttimedb)
        Timer_summary.new_entry_update(username_to_pass)

    def __repr__(self):
        return '<timer/timer startime {!r}, totaltime {!r}, username {!r}'.format(self.starttime, self.totaltime, self.username)

class Timer_summary(db.Model):
    __tablename__ = 'timer_summary'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    entries = db.relationship('Timer_entries', backref='timer_summary', lazy=True)
    daily_average = db.Column(db.Interval)
    total_time = db.Column(db.Interval)

    @classmethod
    def new_entry_update(cls, summary):
        """Simple update of rows parameters, further explained in Timer_entries.entry_setter docstring."""
        totaltimes = [x.totaltime for x in summary.entries]
        total = sum(totaltimes, timedelta())
        average = total / len(totaltimes)
        summary.total_time = total
        summary.daily_average = average
