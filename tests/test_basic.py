import unittest
import requests
import json
import os

from datetime import datetime, timedelta
from flask import current_app

from app import instantiate_app, db
from app.models import Post, Tags, Timer_entries, Timer_summary
from app.timer import ploter

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
        test_post_1 = Post(name="test post 1", description="", description_body="", image="",post_type="project")
        # First test post is project post

        db.session.add(test_tag_1)
        db.session.add(test_tag_2)
        db.session.add(test_post_1)
        db.session.commit()

        for x in range(2, 10): # other post are blogposts
            test_pagination_post = Post(name="test post {}".format(x), description="",
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
        """Seperate function just for the creation of test DB entries.
        While normally there are no direct inserts to the database, as the are handled by they respective setter methods,
        we cannot use them at the setup phase, since they need to be tested as well. If they fail at setup stage, returned
        exceptions will be quite unreadable and as such, it would deafeat the purpose of testing."""

        test_user = Timer_summary(username="test")
        db.session.add(test_user)
        db.session.commit()
        test_timer_entry_1 = Timer_entries(starttime=datetime(2018, 1, 1, 00, 00, 00, 5), totaltime=timedelta(
            hours=1, microseconds=1), username=test_user.id)
        test_timer_entry_2 = Timer_entries(starttime=datetime(2018, 4, 4, 5, 10, 10, 5), totaltime=timedelta(
            minutes=30, microseconds=0), username=test_user.id)
        test_timer_entry_3 = Timer_entries(starttime=datetime(2018, 5, 30, 10, 10, 10, 0), totaltime=timedelta(
            hours=2, microseconds=10), username=test_user.id)
        db.session.add(test_timer_entry_1)
        db.session.add(test_timer_entry_2)
        db.session.add(test_timer_entry_3)
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

    @staticmethod
    def remove_temp_file(path):
        plot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app/static/{}'.format(path)))
        if os.path.exists(plot_path):
            os.remove(plot_path)

    def test_runtime_test(self):
        data_to_json = json.dumps({"test_data": "test data"})
        response = self.app.post('/timer/v0.1/runtime_test', data=data_to_json, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_db_methods(self):
        pass
        #Timer_entries.entry_setter(starttime=datetime(2018, 1, 2, 00, 00, 00, 5), totaltime=timedelta(
         #   hours=1, microseconds=1), username="test")

    def test_post_data(self):
        starttime = datetime(2018, 1, 1, 00, 00, 00, 5)
        totaltime = timedelta(hours=4, microseconds=1)
        data_to_json = json.dumps({"username": "test", "starttime": str(starttime), "worktime": str(totaltime)})
        response = self.app.post('/timer/v0.1/posttime', data=data_to_json, content_type='application/json')

        expected_response =  {'timer_data_point':
            {
                "success": "true",
                "username": "test",
                "starttime": str(starttime),
                "worktime": str(totaltime)
            }
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), expected_response)

    def test_get_data(self):
        response_base = self.app.get('/timer/v0.1/gettime')
        response_test_user = self.app.get('/timer/v0.1/gettime', query_string={'username': 'test'})

        expected_response_base =  {
                "username": "main",
                "totaltime": '3:30:00.000011'
        }

        expected_response_test_user =  {
                "username": "test",
                "totaltime": '3:30:00.000011'
        }


        self.assertEqual(response_base.status_code, 200)
        self.assertEqual(json.loads(response_base.data), expected_response_base)
        self.assertEqual(response_test_user.status_code, 200)
        self.assertEqual(json.loads(response_test_user.data), expected_response_test_user)

    def test_summary(self):
        response_basic = self.app.get('/timer/summary', query_string={'username': 'test'})
        response_no_user = self.app.get('/timer/summary')
        response_bad_user = self.app.get('/timer/summary', query_string={'username': 'not_exists'})
        self.assertEqual(response_basic.status_code, 200)
        self.assertEqual(response_no_user.status_code, 400)
        self.assertEqual(response_bad_user.status_code, 404)
        TimerTestCase.remove_temp_file('chart-test-30.png')

    def test_plot(self):

        ploter.plot("test")
        ploter.plot("test", 20)
        ploter.plot("test", 120)

        plot_path_1 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app/static/chart-test-30.png'))
        plot_path_2 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app/static/chart-test-20.png'))
        plot_path_3 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app/static/chart-test-120.png'))

        self.assertTrue(os.path.isfile(plot_path_1))
        self.assertTrue(os.path.isfile(plot_path_2))
        self.assertTrue(os.path.isfile(plot_path_3))

        TimerTestCase.remove_temp_file('chart-test-30.png')
        TimerTestCase.remove_temp_file('chart-test-20.png')
        TimerTestCase.remove_temp_file('chart-test-120.png')





