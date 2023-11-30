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
        self.l

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
        LOGIN = getenv("LOGIN", "test")
        TOKEN = getenv("TOKEN", "test")

        usr = User(TOKEN, LOGIN)
        response_status = usr.test_credentials
        self.assertEqual(200, response_status)

    def test_rate_limits(self):
        """Tests if rate limit usage is being recorded
        """
