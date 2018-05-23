"""Database models and definitions."""

from . import db
from datetime import datetime, date
from flask_sqlalchemy import BaseQuery
from sqlalchemy import func, extract
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

    @classmethod
    def lower_tags(cls):
        rv = Post.tags.query.all()
        return rv


    def __repr__(self):
        return '<portfolioprojects/posts {!r}, description {!r}. time_added {!r}>'.format(self.name, self.description,
                                                                                          self.time_added)


class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)


    def __repr__(self):
        return '<tag {!r}>'.format(self.name)

class Timer(db.Model):
    __tablename__ = 'timer'

    entry_id = db.Column(db.Integer, primary_key = True)
    entry_starttime = db.Column(db.DateTime, nullable=False)
    entry_totaltime = db.Column(db.Interval, nullable=False)

    @classmethod
    def entry_starttime_setter(cls, starttime, totaltime):
        dbcheck = Timer.query.filter(extract('day', Timer.entry_starttime) == starttime.day).first()

        if dbcheck:
            dbentrytime = dbcheck.entry_totaltime + totaltime
            dbcheck.entry_totaltime = dbentrytime
        else:
            starttimedb = Timer(entry_starttime=starttime, entry_totaltime=totaltime)
            db.session.add(starttimedb)

    def __repr__(self):
        return '<timer/timer startime {!r}, totaltime {!r}'.format(self.entry_starttime, self.entry_totaltime)