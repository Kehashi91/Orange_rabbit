import os
from app import instantiate_app

app = instantiate_app(os.getenv('FLASK_CONFIG') or 'default')



@app.shell_context_processor
def make_shell_context():
    pass


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

