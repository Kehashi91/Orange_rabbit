import unittest
import requests
import json
from datetime import datetime, timedelta

from flask import current_app
from app import instantiate_app, db
from app.models import Post, Tags, Timer_entries, Timer_summary

class AppBasicTestCase(unittest.TestCase):
    """Tests basic app creation"""

    @classmethod
    def setUpClass(self):
        """App and DB setup, created with setUpClass for performance reasons"""
        self.app = instantiate_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app = self.app.test_client()
        db.create_all()

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


class BlogfolioTestCase(unittest.TestCase):
    """Tests basic app creation"""
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

        for current_iteration in range(1, 10):
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
                          description_body="", image="", )

        with self.assertRaises(ValueError):
            dummy_post.post_type = ""

    def test_post(self):

        test_tag_1 = Tags.query.filter_by(name="test_tag_1").first()
        test_tag_2 = Tags.query.filter_by(name="test_tag_2").first()
        test_post_1 = Post.query.filter_by(name="test post 1").first()

        test_post_1.tags = [test_tag_1, test_tag_2]
        db.session.commit()

        # testing many to many relationship
        self.assertIn(test_tag_1, test_post_1.tags)
        self.assertIn(test_tag_2, test_post_1.tags)
        # basic case sanity check
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
            self.assertNotIn("test post 5", str(pagination_test_second_page.data))  # testing for overlap


class TimerTestCase(unittest.TestCase):
    """Tests proper Timer creation and functionalities."""
    @staticmethod
    def dbsetup():
        """Seperate function just for the creation of test DB entries"""
        test_user = Timer_summary(username="main")
        test_timer_entry_1 = Timer_entries()
        db.session.add(test_user)
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

    def test_runtime_test(self):
        data_to_json = json.dumps({"test_data": "test data"})
        response = self.app.post('/timer/v0.1/runtime_test', data=data_to_json, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_data(self):
        starttime = datetime(2018, 1, 1, 00, 00, 00, 5)
        totaltime = timedelta(hours=1, microseconds=1)
        data_to_json = json.dumps({"start_time": str(starttime), "work_time": str(totaltime)})
        response = self.app.post('/timer/v0.1/posttime', data=data_to_json, content_type='application/json')

        expected_response =  {'timer_data_point':
            {
        "start_time": str(starttime),
        "work_time": str(totaltime)
            }
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), expected_response)

    def test_get_data(self):
        response = self.app.get('/timer/v0.1/gettime')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.decode("utf-8"), '0:00:00')

