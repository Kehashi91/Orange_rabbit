import os
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
    """Convenience command to add/modyfi records in dev DB."""
    newpost = PortfolioProject(name="six", description="ojesu nie mam taguf")
    db.session.add(newpost)
    db.session.commit()

