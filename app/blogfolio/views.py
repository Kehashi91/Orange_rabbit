from flask import render_template, current_app, abort
from . import blogfolio
from .. import db
from ..models import Post

@blogfolio.route('/')
def index():
    projects = Post.query.all()
    return render_template("index.html", projects=projects)

@blogfolio.route('/<project>')
def show_project(project):
    project = Post.query.filter_by(name=project).first_or_404()
    return render_template("project.html", project=project)

@blogfolio.route('/blog')
def blog():
    return render_template("blog.html")
