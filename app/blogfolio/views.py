"""Routes and view functions for Blog and portfolio"""

from flask import render_template, request
from flask_sqlalchemy import Pagination
from . import blogfolio
from .. import db
from ..models import Post

@blogfolio.route('/')
def index():
    projects = Post.query.filter_by(post_type="project").all()
    return render_template("index.html", projects=projects)

@blogfolio.route('/<project>')
def show_project(project):
    """ Includes workaround to avoid whitespace in url.
    The app will still accept whitespaces in url, but they can 
    only appear if explicitly typed."""
    
    project_unurlize = project.replace("-", " ")
    project = Post.query.filter_by(name=project_unurlize).first_or_404()

    return render_template("project.html", project=project)

@blogfolio.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(post_type="blogpost").paginate(page, 5, True)
    return render_template("blog.html", posts=posts)

@blogfolio.route('/search')
def search():
    search_query = request.args.get('search', 'nothing')
    return render_template("search.html", search=search_query)
