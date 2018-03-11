from . import db
from datetime import datetime


class PortfolioProject(db.Model):
    __tablename__ = "portfolioprojects"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    time_added = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Portfolioroject {!r}, description {!r}. time_added {!r}>'.format(self.title, self.name, self.time_added)

class Tags(db.Model):
    __tablename = "tags"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)