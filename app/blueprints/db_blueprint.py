#!/usr/bin/python3

"""
Controls operations dealing with mongodb

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""

from flask import Blueprint, jsonify, request, session, url_for, redirect
from modules.user import User
from modules.mongo_crud import doc_signup, doc_login  # noqa
from flask_pymongo import PyMongo

# Create a Flask Blueprint
db_bp = Blueprint('db', __name__)

# Initialize PyMongo within the Blueprint
mongo = PyMongo()


@db_bp.route('/', strict_slashes=False, methods=["GET"])
def db_status():
    """checks db status by listing collections"""
    return jsonify(mongo.db.list_collection_names())


@db_bp.route('/signup', strict_slashes=False, methods=["POST"])
def db_signup():
    """add's new user and their details to the database, authenticates users
    data in the process"""
    try:
        json_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "token": request.form.get("token"),
            "login": request.form.get("login")
        }

        response = doc_signup(mongo.db.users, json_data)
        return jsonify({"message": response[0]}), response[1]
    except Exception as e:
        return jsonify({"message": e}), 400


@db_bp.route('/login', strict_slashes=False, methods=["GET", "POST"])
def db_login():
    """logs a new user into the user database"""
    try:
        json_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password")
        }

        response = doc_login(mongo.db.users, json_data)
        if response[1] == 200:

            # get user info from login information
            user = User(response[0]["token"], response[0]["login"])
            all_info = user.get_all_info()
            # load the info into the session
            for key, value in all_info.items():
                session[key] = value
            session["token"] = response[0]["token"]
            return redirect(url_for("dashboard"))
        else:
            return jsonify({"message": response[0]}), response[1]
    except Exception as e:
        return jsonify({"message": e}), 400
