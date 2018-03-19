import os
from flask import render_template
from app import instantiate_app, db
from app.models import PortfolioProject, Tags
from flask_migrate import Migrate

app = instantiate_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, PortfolioProject=PortfolioProject, Tags=Tags)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def add_recort():
    thetag1 = PortfolioProject.query.filter_by(name='six').first()
    thetag1.image = "media/BigIcon.png"
    thetag2 = PortfolioProject.query.filter_by(name='pionc').first()
    thetag2.image = "media/ping.gif"
    thetag3 = PortfolioProject.query.filter_by(name='czwarty!').first()
    thetag3.image = "media/nginx-9.jpg"
    db.session.commit()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404