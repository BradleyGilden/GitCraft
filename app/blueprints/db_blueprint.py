#!/usr/bin/python3

"""
Controls operations dealing with mongodb

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""

from flask import Blueprint, jsonify, request, session, url_for, redirect
from app.modules.user import User
from app.modules.mongo_crud import doc_signup, doc_login, doc_update
from app.modules.security import hash_password, decrypt_token
from app.config import ICON_PACK, ICON_PACK1, ICON_PACK2, SESSION_KEYS
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
            "password": hash_password(request.form.get("password")),
            "token": request.form.get("token"),
            "login": request.form.get("login"),
            "langs": [],
            "tools": []
        }

        response = doc_signup(mongo.db.users, json_data)
        return jsonify({"message": response[0]}), response[1]
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@db_bp.route('/login', strict_slashes=False, methods=["GET", "POST"])
def db_login():
    """logs a new user into the user database"""
    try:
        json_data = {
            "username": request.form.get("username"),
            "password": hash_password(request.form.get("password"))
        }

        response = doc_login(mongo.db.users, json_data)
        if response[1] == 200:
            # decrypt token from the database
            response[0]["token"] = decrypt_token(response[0]["token"])
            # get user info from login information
            user = User(response[0]["token"], response[0]["login"])
            all_info = user.get_all_info()
            if (all_info is None):
                raise Exception("Bad Credentials")
            # keep session open for 24 hours after login
            session.permanent = True
            # load the info into the session
            for key, value in all_info.items():
                session[key] = value
            session["langs"] = response[0]["langs"]
            session["tools"] = response[0]["tools"]
            session["token"] = response[0]["token"]
            session["gitcraft_user"] = json_data["username"]
            session["socialicons"] = ICON_PACK
            session["socialicons1"] = ICON_PACK1
            session["socialicons2"] = ICON_PACK2
            return redirect(url_for("dashboard"))
        else:
            return jsonify({"message": response[0]}), response[1]
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@db_bp.route('/logout', strict_slashes=False, methods=["POST"])
def db_logout():
    """releases data from session"""
    for data in SESSION_KEYS:
        session.pop(data, None)
    session.permanent = False
    return redirect(url_for('authentication')), 302


@db_bp.route('/update', strict_slashes=False, methods=["PUT"])
def db_update():
    """updates a users custom details"""
    try:
        default_data = {"langs": session["langs"], "tools": session["tools"]}
        custom_data = request.get_json()
        response = doc_update(mongo.db.users, session["gitcraft_user"],
                              custom_data, default_data)
        if response[1] < 400:
            session["langs"] = response[0]["langs"]
            session["tools"] = response[0]["tools"]
            return jsonify({"message": response[0]}), response[1]
        else:
            return jsonify({"message": response[0]}), response[1]
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@db_bp.route('/refresh', strict_slashes=False, methods=["GET"])
def db_refresh():
    """refreshes information from github"""
    try:
        user = User(session["token"], session["login"])
        all_info = user.get_all_info()
        # load the info into the session
        for key, value in all_info.items():
            session[key] = value
        return jsonify({"message": "success"}), 200
    except Exception:
        return jsonify({"message": "failure"}), 400
