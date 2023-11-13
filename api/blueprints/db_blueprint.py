#!/usr/bin/python3

"""
Controls operations dealing with mongodb

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""

from flask import Blueprint, jsonify
from flask_pymongo import PyMongo

# Create a Flask Blueprint
db_bp = Blueprint('db', __name__)

# Initialize PyMongo within the Blueprint
mongo = PyMongo()


@db_bp.route('/', strict_slashes=False, methods=["GET"])
def db_status():
    """checks db status by listing collections"""
    return jsonify(mongo.db.list_collection_names())
