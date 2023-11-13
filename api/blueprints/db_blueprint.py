#!/usr/bin/python3

"""
Controls operations dealing with mongodb

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""

from flask import Blueprint, jsonify, request
from modules.mongo_crud import insert_doc  # noqa
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
    """add's new user and their details to the database"""
    try:
        json_data = request.get_json()
        response = insert_doc(mongo.db.users, json_data)
        if response != "write error" and response != "occupied":
            return jsonify({"message": response}), 200
        else:
            return jsonify({"message": response}), 400
    except Exception as e:
        return jsonify({"message": e}), 400
