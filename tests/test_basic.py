import unittest

from flask import current_app
from app import instantiate_app

class AppBasicTestCase(unittest.TestCase):
    """Tests proper app creation"""

    def setUp(self):
        self.app = instantiate_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


class PageRenderTestCase(unittest.TestCase):
    """Tests rendering of templates/pages"""

    def setUp(self):
        self.app = instantiate_app('testing')
        self.app = self.app.test_client()


    def test_helloworld(self):
        rv = self.app.get('/')
        self.assertIn('hello world!', str(rv.data))
