from . import db
from datetime import date


metatags = db.Table('metatags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('portfolioprojects.project_id'), primary_key=True)
)

class PortfolioProject(db.Model):
    __tablename__ = "portfolioprojects"
    project_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    time_added = db.Column(db.Date, nullable=False, default=date.today())
    #subpage_html = db.columnn(db.Text)
    tags = db.relationship('Tags', secondary=metatags, lazy='subquery',
        backref=db.backref('portfolioprojects', lazy=True))

    def __repr__(self):
        return '<portfolioprojects {!r}, description {!r}. time_added {!r}>'.format(self.name, self.description, self.time_added)

class Tags(db.Model):
    __tablename = "tags"
    tag_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)

    def __repr__(self):
        return '<tag {!r}>'.format(self.name)

