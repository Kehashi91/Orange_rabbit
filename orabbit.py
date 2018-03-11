import os
from app import instantiate_app, db
from app.models import PortfolioProject
from flask_migrate import Migrate

app = instantiate_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, PortfolioProject=PortfolioProject)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def add_recort():
    newpost = PortfolioProject(name="tester", description="kolejne testy, wiele testow!")
    db.session.add(newpost)
    db.session.commit()

