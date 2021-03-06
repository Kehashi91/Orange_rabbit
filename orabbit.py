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
    ---> timer - timer blueprint directory
    -> __init__ - Blueprint initialization
    -> views.py - view functions and simple API calls
"""

import os
import click

from flask import render_template
from flask_migrate import Migrate

from app import instantiate_app, db, mail
from app.models import Post, Tags


app = instantiate_app(os.getenv('FLASK_ENV') or 'development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Tags=Tags, mail=mail)


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
def setup_db():
    """Convenience method for adding/modyfing database entries during development"""
    db.create_all()

@app.cli.command()
@click.option("--filename", default=None, help="Filename of input csv file")
@click.option("--tags", default=None, help="List of tags to be added")
def add_record(filename, tags):
    """Temporary method for adding records until I make a simple CMS."""
    db.create_all()

    if tags:
        for tag in tags.split(","):
            db_insert = Tags(name=tag)
            db.session.add(db_insert)
            db.session.commit()

    if filename:
        import csv
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print (row)
                kwargs = {key:value for (key, value) in row.items()}
                kwargs["tags"] = [Tags.query.filter_by(name=tag).first() for tag in kwargs["tags"].split(",")]
                db_insert = Post(**kwargs)
                db.session.add(db_insert)
                db.session.commit()

@app.cli.command()
def db_command():
    """Convenience method for adding/modyfing database entries during development"""
    post = Post.query.filter_by(name="dns-utils").first()
    db.session.delete(post)
    db.session.commit()

@app.errorhandler(404)
def page_not_found(e):
    """Errorhandlers needs to be implemented at app layer, not blueprint layer."""
    return render_template("404.html"), 404