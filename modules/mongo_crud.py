#!/usr/bin/python3

"""
creates functions for crud operations

Author: Bradley Dillion Gilden
Date: 09-11-2023
"""
from modules.user import User
from pymongo.errors import BulkWriteError, WriteError  # noqa
from bson import ObjectId  # noqa


def doc_signup(collection, document: dict) -> list:
    """signs a user up to gitcraft by inserting a document"""
    try:
        user = User(document["token"], document["login"])
        if user.test_credentials != 200:
            return ["invalid credentials (token or github username)", 400]
        doc = collection.find_one({"username": document["username"]})
        if doc is None:
            doc_id = collection.insert_one(document).inserted_id
            return [str(doc_id), 200]
        else:
            return ["usernamee taken", 400]
    except WriteError:
        return ["WriteError", 400]


def doc_login(collection, document: dict) -> list:
    """confirms login of a user by checking document entries"""
    doc = collection.find_one({"username": document["username"]})
    if doc is None or doc["password"] != document["password"]:
        return ["invalid_credentials", 400]
    else:
        return [doc, 200]
