"""blueprint initialization."""

from flask import Blueprint

timer = Blueprint('timer', __name__)

from . import views