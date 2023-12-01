#!/usr/bin/python3

"""
Tests methods that interact with MongoDB

Author: Bradley Dillion Gilden
Date: 30-11-2023
"""


import unittest
from os import getenv
from pymongo import MongoClient
from app.config import DATABASE_URL
from app.modules.mongo_crud import doc_signup, doc_login


class TestDB(unittest.TestCase):
    """tests database operations"""

    def setUp(self) -> None:
        """Sets up MongoDB client"""
        self.client = MongoClient(DATABASE_URL)
        self.collection = self.client.gitcraft.users
        self.LOGIN = getenv("LOGIN", "test")
        self.USER = getenv("USER", "test")
        self.TOKEN = getenv("TOKEN", "test")

    def test_connection(self):
        """checks connection by seeing if collection actually exists on the
        database"""
        self.assertIn("users", self.client.gitcraft.list_collection_names())

    def test_signup(self):
        """tests signup validation with mongodb client"""
        message = doc_signup(self.collection,
                             {"token": self.TOKEN,
                              "login": self.LOGIN,
                              "username": self.USER})
        self.assertTrue(message[1] == 200 or message[0] == "username taken")

    def test_signup_invalid_credentials(self):
        """tests for instance where github username and token do not match"""
        message = doc_signup(self.collection,
                             {"token": "1234",
                              "login": self.LOGIN,
                              "username": self.USER})
        self.assertEqual(message[0],
                         "invalid credentials (token or github username)")

    def test_login_invalid_credentials(self):
        """tests for unverified login"""
        message = doc_login(self.collection, {"username": "Test",
                                              "password": "1234"})
        self.assertEqual(message[1], 400)

    def test_login_valid_credentials(self):
        """tests for verified login"""
        message = doc_login(self.collection, {
            "username": "Test",
            "password": "ThisIsATestPassword123"
            })
        self.assertEqual(message[1], 200)
