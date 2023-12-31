#!/usr/bin/python3

"""
Test module for the user class

Author: Bradley Dillion Gilden
Date: 30-11-2023
"""


import unittest
from app.modules import user
from app.modules.user import User
from os import getenv
from requests import get  # noqa


class TestUser(unittest.TestCase):
    """Test Class for the user class"""

    def setUp(self):
        self.LOGIN = getenv("LOGIN", "test")
        self.TOKEN = getenv("TOKEN", "test")

    def test_module_documentation(self):
        """tests that user module is documented"""
        self.assertGreater(len(user.__doc__), 1)

    def test_property_documentation(self):
        """tests that User class properties are documented"""
        self.assertGreater(len(User.num_commits.__doc__), 1)
        self.assertGreater(len(User.info.__doc__), 1)
        self.assertGreater(len(User.socials.__doc__), 1)
        self.assertGreater(len(User.streak_stats.__doc__), 1)
        self.assertGreater(len(User.test_credentials.__doc__), 1)
        self.assertGreater(len(User.space_occupied.__doc__), 1)
        self.assertGreater(len(User.rate_limits.__doc__), 1)

    def test_method_documentation(self):
        """Tests that user methods are documented"""
        self.assertGreater(len(User.__init__.__doc__), 1)
        self.assertGreater(len(User.calculate_streak_stats.__doc__), 1)
        self.assertGreater(len(User.get_all_info.__doc__), 1)
        self.assertGreater(len(User.info_update.__doc__), 1)
        self.assertGreater(len(User.pinned_repos.__doc__), 1)
        self.assertGreater(len(User.socials_update.__doc__), 1)

    def test_credentials(self):
        """tests credentials of a user"""
        usr = User(self.TOKEN, self.LOGIN)
        response_status = usr.test_credentials
        self.assertEqual(200, response_status)

    def test_incorrect_credentials(self):
        """tests if github is denying wrong credentials"""
        usr = User("test", "test")
        response_status = usr.test_credentials
        self.assertGreaterEqual(response_status, 400)

    def test_rate_limits(self):
        """Tests if rate limit usage is being recorded
        """
        usr = User(self.TOKEN, self.LOGIN)
        # get current rate limit
        rate_old = usr.rate_limits
        # make request to increase rate limit
        usr.get_all_info()
        rate_new = usr.rate_limits
        self.assertGreater(rate_new["rest"]["used"], rate_old["rest"]["used"])
        self.assertGreater(
            rate_new["graphql"]["used"], rate_old["graphql"]["used"])

    def test_num_commits(self):
        """tests if integer is being returned when num_commits succeeeds"""
        usr = User(self.TOKEN, self.LOGIN)
        commits = usr.num_commits
        self.assertEqual(type(commits), int)
        self.assertGreaterEqual(commits, 0)

    def test_num_commits_fail(self):
        """tests for when num_commits fails"""
        usr = User("test", "test")
        commits = usr.num_commits
        self.assertEqual(commits, {})

    def test_pinned_fail(self):
        """tests for output when pinned items fail"""
        usr = User(self.TOKEN, self.LOGIN)
        self.assertRaises(TypeError, usr.pinned_repos, "test")

    def test_pinned_success(self):
        """tests for output when query is succesful"""
        usr = User(self.TOKEN, self.LOGIN)
        response = usr.pinned_repos(3)
        self.assertEqual(type(response), list)

    def test_streak_stats(self):
        """Tests if streak stat data is logical and of the correct format"""
        usr = User(self.TOKEN, self.LOGIN)
        stats = usr.streak_stats
        self.assertEqual(type(stats["current"]), int)
        self.assertEqual(type(stats["longest"]), int)
        self.assertEqual(type(stats["total"]), int)
        self.assertGreaterEqual(stats["total"], stats["longest"])
        self.assertGreaterEqual(stats["longest"], stats["current"])

    def test_space_occupied_type(self):
        """tests value type in response of space_occupied"""
        usr = User(self.TOKEN, self.LOGIN)
        space = usr.space_occupied
        self.assertEqual(type(space), int)

    def test_user_info(self):
        """test if correct user information is returned"""
        usr = User(self.TOKEN, self.LOGIN)
        info = usr.info
        self.assertEqual(info["login"], self.LOGIN)

    def test_user_info_all(self):
        """check if the all method is adapting the required values from other
        methods"""
        usr = User(self.TOKEN, self.LOGIN)
        info_all = usr.get_all_info()

        self.assertIn("login", info_all)
        self.assertEqual(info_all["login"], self.LOGIN)
        self.assertEqual(type(info_all["repo_space"]), int)
