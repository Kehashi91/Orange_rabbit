"""Routes and view functions for Blog and portfolio

TODO: Once I have 5+ projects, add pagination to index."""

from flask import render_template, request, abort
from flask_sqlalchemy import Pagination
from sqlalchemy import or_, func
from . import blogfolio
from ..models import Post, Tags

@blogfolio.route('/')
def index():
    """Home page, lists all projects"""
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
    """Blog site with default pagination. Projects included with a special tag."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, 5, True)
    tags = Tags.query.all()
    tags_half_1 = tags[int(len(tags)/2):]
    tags_half_2 = tags[:int(len(tags)/2)]

    return render_template("blog.html", posts=posts, tags1=tags_half_1, tags2=tags_half_2, paginate_url="blog?")

@blogfolio.route('/search')
def search():
    """Simple search by text and tags."""
    search_query = request.args.get('query')
    page = request.args.get('page', 1, type=int)


    if not search_query:
        abort(404)
    else:
        results = Post.query.filter(or_(func.lower(Post.name).like(('%' + search_query + '%').lower()),
                                        Post.tags.any(name=search_query)))
        results_count = results.count()
        results_paginate = results.paginate(page, 5, True)

        return render_template("search.html", query=search_query, results=results_paginate, count=results_count,
                               paginate_url="search?query=test&")
