from flask import render_template, current_app
from . import blogfolio
from .. import db
from ..models import PortfolioProject

@blogfolio.route('/')
def index():
    projects = PortfolioProject.query.all()
    return render_template("index.html", projects=projects)


