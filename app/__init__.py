from flask import Flask
from config import config

def instantiate_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .blogfolio import blogfolio as blogfolio_blueprint
    app.register_blueprint(blogfolio_blueprint)

    return app

