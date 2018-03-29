import unittest

from flask import current_app
from app import instantiate_app, db

class AppBasicTestCase(unittest.TestCase):
    """Tests proper app creation"""

    def setUp(self):
        self.app = instantiate_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.app = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_porfolio_homepage(self):
        template_to_test = self.app.get('/')
        self.assertIn('<div class="invisible">fjfe95yskl1SDFA113</div>', str(template_to_test.data))
