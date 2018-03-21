from . import db
from datetime import date
from sqlalchemy.orm import validates



metatags = db.Table('metatags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "post"


    post_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    time_added = db.Column(db.Date, nullable=False, default=date.today())
    #subpage_html = db.columnn(db.Text)
    tags = db.relationship('Tags', secondary=metatags, lazy='subquery',
        backref=db.backref('Post', lazy=True))
    post_type = db.Column(db.Text, nullable=False)

    @validates('post_type')
    def validate_post_type(self, key, post_type):
        post_types_reference = {"project", "blogpost"}
        if post_type in post_types_reference:
            return post_type
        else:
            raise ValueError("Post type must be: {!r}".format(post_types_reference))


    def __repr__(self):
        return '<portfolioprojects/posts {!r}, description {!r}. time_added {!r}>'.format(self.name, self.description, self.time_added)


class Tags(db.Model):
    __tablename = "tags"
    tag_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)

    def __repr__(self):
        return '<tag {!r}>'.format(self.name)


