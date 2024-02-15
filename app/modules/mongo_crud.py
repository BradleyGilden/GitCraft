#!/usr/bin/python3

"""
creates functions for crud operations

Author: Bradley Dillion Gilden
Date: 09-11-2023
"""
from app.modules.user import User
from pymongo.errors import WriteError
from app.modules.security import encrypt_token


def doc_signup(collection, document: dict) -> list:
    """signs a user up to gitcraft by inserting a document"""
    try:
        user = User(document["token"], document["login"])
        if user.test_credentials != 200:
            return ["invalid credentials (token or github username)", 400]
        doc = collection.find_one({"username": document["username"]})
        if doc is None:
            # encrypt token for extra layer of security
            document["token"] = encrypt_token(document["token"])
            doc_id = collection.insert_one(document).inserted_id
            return [str(doc_id), 200]
        else:
            return ["username taken", 400]
    except WriteError:
        return ["WriteError", 400]


def doc_login(collection, document: dict) -> list:
    """confirms login of a user by checking document entries"""
    doc = collection.find_one({"username": document["username"]})
    if doc is None or doc["password"] != document["password"]:
        return ["invalid_credentials", 400]
    else:
        return [doc, 200]


def doc_update(collection, username, document: dict, default: dict) -> list:
    """updates customized details of a user"""
    try:
        doc = collection.update_one({"username": username},
                                    {
                                        "$set": {
                                            "langs": document["langs"],
                                            "tools": document["tools"]
                                        }
                                    },
                                    upsert=True)
        if doc.modified_count > 0:
            doc = collection.find_one({"username": username})
            return [{"langs": doc["langs"], "tools": doc["tools"]}, 200]
        else:
            return [{"langs": default["langs"], "tools": default["tools"]},
                    204]
    except WriteError:
        return ["WriteError", 400]
