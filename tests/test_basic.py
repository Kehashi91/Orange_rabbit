import unittest
import os

from flask import current_app
from app import instantiate_app, db
from app.models import Post, Tags

class AppBasicTestCase(unittest.TestCase):
    """Tests proper app creation and functionalities."""

    @staticmethod
    def dbsetup():
        """Seperate function just for the creation of test DB entries"""
        test_tag_1 = Tags(name="test_tag_1")
        test_tag_2 = Tags(name="test_tag_2")
        test_post_1 = Post(name="test post 1", description="",
                           description_body="", image="",
                           post_type="project")

        db.session.add(test_tag_1)
        db.session.add(test_tag_2)
        db.session.add(test_post_1)
        db.session.commit()

        for current_iteration in range(2, 10):
            test_pagination_post = Post(name="test post {}".format(current_iteration), description="",
                               description_body="", image="",
                               post_type="blogpost")
            db.session.add(test_pagination_post)
            db.session.commit()


    @classmethod
    def setUpClass(self):
        """App and DB setup, created with setUpClass for performance reasons"""
        self.app = instantiate_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()
        self.dbsetup()

    @classmethod
    def tearDownClass(self):
        """Clean teardown at finished tests."""
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

    def test_url_workaround(self):
        url_whitespace_url = self.app.get('/test post 1')
        url_dash_url = self.app.get('/test-post-1')
        url_false = self.app.get('/kfk131nnphpzev1g98g5')
        self.assertEqual(url_whitespace_url.status_code, 200)
        self.assertEqual(url_dash_url.status_code, 200)
        self.assertEqual(url_false.status_code, 404)

    def test_tag(self):
        verify_query_tag_1 = Tags.query.filter_by(name="test_tag_1").first()
        verify_query_tag_2 = Tags.query.filter_by(name="test_tag_2").first()
        dummy_query = Tags.query.filter_by(name="Nonexistent_tag").first()

        self.assertIsNotNone(verify_query_tag_1.tag_id)
        self.assertEqual(verify_query_tag_1.name, "test_tag_1")
        self.assertIsNotNone(verify_query_tag_2.tag_id)
        self.assertEqual(verify_query_tag_2.name, "test_tag_2")
        self.assertIsNone(dummy_query)


    def test_post_validator(self):

        dummy_post = Post(name="test_dummy", description="",
                           description_body="", image="",)

        with self.assertRaises(ValueError):
            dummy_post.post_type = ""

    def test_post(self):


        test_tag_1 = Tags.query.filter_by(name="test_tag_1").first()
        test_tag_2 = Tags.query.filter_by(name="test_tag_2").first()
        test_post_1 = Post.query.filter_by(name="test post 1").first()

        test_post_1.tags = [test_tag_1, test_tag_2]
        db.session.commit()

        #testing many to many relationship
        self.assertIn(test_tag_1, test_post_1.tags)
        self.assertIn(test_tag_2, test_post_1.tags)
        #basic case sanity check
        self.assertIsNotNone(test_post_1.post_id)
        self.assertEqual(test_post_1.name, "test post 1")

    def test_pagination(self):
        pagination_test = self.app.get('/blog')
        pagination_test_second_page = self.app.get('/blog?page=2')

        for x in range(1, 5):
            self.assertIn("test post {}".format(x), str(pagination_test.data))
        self.assertNotIn("test post 6", str(pagination_test.data))

        for x in range(6, 10):
            self.assertIn("test post {}".format(x), str(pagination_test_second_page.data))
            self.assertNotIn("test post 5", str(pagination_test_second_page.data)) #testing for overlap
