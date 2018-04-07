"""blueprint initialization."""

from flask import Blueprint

blogfolio = Blueprint('blogfolio', __name__)

from . import views