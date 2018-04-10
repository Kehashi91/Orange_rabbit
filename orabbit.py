"""
Main script for app initialization and CLI interface.

Application structure:
-> orabbit.py - this file
-> config.py - configuration classes
-> requirements.txt - Lists all packages and dependencies
-> migrations - Flask-migrate directory
-> env - venv directory
 ---> app - Main app directory
   -> __init__ - App initialization 
   -> models - Database models and definitions
    ---> static - Static files directory
    ---> templates - Templates directory
    ---> blogfolio - blogfolio blueprint directory
      -> __init__ - Blueprint initialization
      -> views.py - view functions
"""

import os
from flask import render_template
from app import instantiate_app, db
from app.models import Post, Tags
from flask_migrate import Migrate

app = instantiate_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Tags=Tags)


@app.cli.command()
def test():
    """Run the unit tests."""
    if app.config["TESTING"] == True:
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
    else:
        raise KeyError("Wrong app configuration: FLASK_CONFIG must be 'testing'")

@app.cli.command()
def add_record():
    """Convenience method for adding/modyfing database entries durgin development"""
    test_tag_1 = Tags.query.filter_by(name="Python").first()
    test_tag_2 = Tags.query.filter_by(name="CSS").first()
    test_tag_3 = Tags.query.filter_by(name="HTML").first()
    test_post_1 = Post.query.filter_by(name="Post nr 0").first()

    test_post_1.tags = [test_tag_1, test_tag_2, test_tag_3]

@app.errorhandler(404)
def page_not_found(e):
    """Errorhandlers needs to be implemented at app layer, not blueprint layer."""
    return render_template("404.html"), 404