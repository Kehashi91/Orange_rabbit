from flask import render_template, request
from flask_sqlalchemy import Pagination
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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, 5, False)
    return render_template("blog.html", posts=posts.items)
