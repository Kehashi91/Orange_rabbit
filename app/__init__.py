"""App initialization."""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

db = SQLAlchemy()
mail = Mail()

def instantiate_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    mail.init_app(app)


    from .blogfolio import blogfolio as blogfolio_blueprint
    from .timer import timer as timer_blueprint

    app.register_blueprint(blogfolio_blueprint)
    app.register_blueprint(timer_blueprint, url_prefix='/timer')

    return app

