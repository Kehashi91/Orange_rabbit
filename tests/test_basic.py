import unittest
import os

from flask import current_app
from app import instantiate_app, db
from app.models import Post, Tags

class AppBasicTestCase(unittest.TestCase):
    """Tests proper app creation and functionalities."""

    @classmethod
    def setUpClass(self):
        """App and DB setup, created with setUpClass for performance reasons"""
        self.app = instantiate_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.app = self.app.test_client()

    @classmethod
    def tearDownClass(self):
        """Clean teardown at finished tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Verifies proper configuration loading."""
        self.assertTrue(current_app.config['TESTING'])

    def test_porfolio_homepage(self):
        """tests basic template rendering"""
        template_to_test = self.app.get('/')
        self.assertIn('<div class="invisible">fjfe95yskl1SDFA113</div>', str(template_to_test.data))

    def test_tag(self):
        """sanity check for Tags table."""
        test_tag_1 = Tags(name="test_tag_1")
        test_tag_2 = Tags(name="test_tag_2")

        db.session.add(test_tag_1)
        db.session.add(test_tag_2)


        verify_query_tag_1 = Tags.query.filter_by(name="test_tag_1").first()
        verify_query_tag_2 = Tags.query.filter_by(name="test_tag_2").first()
        dummy_query = Tags.query.filter_by(name="Nonexistent_tag").first()

        self.assertIsNotNone(verify_query_tag_1.tag_id)
        self.assertEqual(verify_query_tag_1.name, "test_tag_1")
        self.assertIsNotNone(verify_query_tag_2.tag_id)
        self.assertEqual(verify_query_tag_2.name, "test_tag_2")
        self.assertIsNone(dummy_query)



    def test_post(self):
        """Basic test for Post, veryfing validators and Many to many relation with tags"""
        test_post_1 = Post(name="test_Post_2", description="test_Post_1 short description",
                           description_body="test_Post_1 long description", image="testimage1",
                           post_type="project")
        test_post_2 = Post(name="test_Post_2", description="test_Post_2 short description",
                           description_body="test_Post_2 long description", image="testimage2",
                           post_type="blogpost")
        dummy_post = Post(name="test_dummy", description="",
                           description_body="", image="",)

        test_tag_3 = Tags(name="test_tag_3")
        test_tag_4 = Tags(name="test_tag_4")

        db.session.add(test_tag_3)
        db.session.add(test_tag_4)

        with self.assertRaises(ValueError):
            dummy_post.post_type = ""

        test_post_1.tags = [test_tag_3, test_tag_4]

        self.assertIn(test_tag_3, test_post_1.tags)
        self.assertIn(test_tag_4, test_post_1.tags)


"""
    post_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_body = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    time_added = db.Column(db.Date, nullable=False, default=date.today())
    tags = db.relationship('Tags', secondary=metatags, lazy='subquery',
        backref=db.backref('Post', lazy=True))
    post_type = db.Column(db.Text, nullable=False)
    """
