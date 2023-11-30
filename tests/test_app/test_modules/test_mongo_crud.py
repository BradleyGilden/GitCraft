#!/usr/bin/python3

"""
Tests methods that interact with MongoDB

Author: Bradley Dillion Gilden
Date: 30-11-2023
"""


import unittest
from pymongo import MongoClient
from app.config import DATABASE_URL


class TestDB(unittest.TestCase):
    """tests database operations"""

    def setUp(self) -> None:
        self.client = MongoClient(DATABASE_URL)
        self.collection = self.client.gitcraft.users

    def test_connection(self):
        """checks connection by seeing if collection actually exists on the
        database"""
        self.assertIn("users", self.client.gitcraft.list_collection_names())
