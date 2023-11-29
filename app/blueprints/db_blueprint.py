#!/usr/bin/python3

"""
Controls operations dealing with mongodb

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""

from flask import Blueprint, jsonify, request, session, url_for, redirect
from app.modules.user import User
from app.modules.mongo_crud import doc_signup, doc_login, doc_update  # noqa
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
            "login": request.form.get("login"),
            "langs": [],
            "tools": []
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
            session["langs"] = response[0]["langs"]
            session["tools"] = response[0]["tools"]
            session["token"] = response[0]["token"]
            session["gitcraft_user"] = json_data["username"]
            session["socialicons"] = {
                "instagram":
                "https://img.icons8.com/color/48/instagram-new--v1.png",
                "facebook":
                "https://img.icons8.com/fluency/48/facebook-new.png",
                "linkedin": "https://img.icons8.com/color/48/linkedin.png",
                "twitter": "https://img.icons8.com/color/48/twitter--v1.png",
                "reddit": "https://img.icons8.com/doodle/48/reddit--v4.png",
                "telegram": "https://img.icons8.com/color/48/telegram-app.png",
                "discord": "https://img.icons8.com/color/48/discord-logo.png",
                "snapchat": "https://img.icons8.com/doodle/48/snapchat.png",
                "default": "https://img.icons8.com/ios/50/circled.png"
            }
            session["socialicons1"] = {
                "instagram":
                "https://img.icons8.com/ios-filled/50/instagram-new--v1.png",
                "facebook":
                "https://img.icons8.com/ios-filled/50/facebook-new.png",
                "linkedin":
                "https://img.icons8.com/ios-filled/50/linkedin.png",
                "twitter": "https://img.icons8.com/ios-filled/50/twitter.png",
                "reddit":
                "https://img.icons8.com/ios-filled/50/reddit--v1.png",
                "telegram":
                "https://img.icons8.com/ios-filled/50/telegram-app.png",
                "discord":
                "https://img.icons8.com/ios-filled/50/discord-logo.png",
                "snapchat":
                "https://img.icons8.com/ios-filled/50/snapchat--v1.png",
                "default": "https://img.icons8.com/ios/50/circled.png"
            }
            session["socialicons2"] = {
                "instagram": "ri-instagram-fill",
                "facebook": "ri-facebook-circle-fill",
                "linkedin": "ri-linkedin-fill",
                "twitter": "ri-twitter-fill",
                "reddit": "ri-reddit-fill",
                "telegram": "ri-telegram-fill",
                "discord": "ri-discord-fill",
                "snapchat": "ri-snapchat-fill",
                "default": "ri-circle-fill"
            }
            return redirect(url_for("dashboard"))
        else:
            return jsonify({"message": response[0]}), response[1]
    except Exception as e:
        return jsonify({"message": e}), 400


@db_bp.route('/logout', strict_slashes=False, methods=["POST"])
def db_logout():
    """handles logout of a user"""
    session_data = {
        "login", "avatar", "name", "company", "blog", "location", "email",
        "hireable", "bio", "space_available", "plan", "following", "followers",
        "repo_count", "created_at", "repo_space", "socials", "streak",
        "pinned", "token", "gitcraft_user", "langs", "tools"
    }
    # releases data from session
    for data in session_data:
        session.pop(data, None)
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
        return jsonify({"message": e}), 400


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
