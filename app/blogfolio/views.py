from flask import render_template, current_app
from . import blogfolio

@blogfolio.route('/')
def index():
    return "<b>hello world!</b>"