#!/usr/bin/python3

"""
This blue print will handle github requests

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""


from app.modules.user import User
from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)


@api_bp.route("/", strict_slashes=False)
def status():
    """Tests if API is active"""
    return jsonify({"status": "OK"})


@api_bp.route("/user", strict_slashes=False, methods=["GET"])
def get_user_info():
    """This function returns basic user information"""
    headers = dict(request.headers)
    if headers.get("Token") is None or headers.get("Username") is None:
        return jsonify({"message": "Token or Username Header missing"}), 400
    user = User(request.headers.get("Token"), request.headers.get("Username"))
    return jsonify(user.info)


@api_bp.route("/user/commits", strict_slashes=False, methods=["GET"])
def get_commits():
    """This function returns basic user information"""
    headers = dict(request.headers)
    if headers.get("Token") is None or headers.get("Username") is None:
        return jsonify({"message": "Token or Username Header missing"}), 400
    user = User(request.headers.get("Token"), request.headers.get("Username"))
    return jsonify(user.num_commits)


@api_bp.route("/pinned/<int:num>", strict_slashes=False, methods=["GET"])
def get_pinned_repos(num):
    """This function will <num> number of pinned repositories and their
    corresponding info
    """
    headers = dict(request.headers)
    if headers.get("Token") is None or headers.get("Username") is None:
        return jsonify({"message": "Token or Username Header missing"}), 400
    user = User(request.headers.get("Token"), request.headers.get("Username"))
    return jsonify(user.pinned_repos(num))


@api_bp.route("/user/update", strict_slashes=False, methods=["PATCH"])
def patch_user_info():
    """This function will <num> number of pinned repositories and their
    corresponding info
    """
    headers = dict(request.headers)
    data = request.get_json()
    if headers.get("Token") is None or headers.get("Username") is None:
        return jsonify({"message": "Token or Username Header missing"}), 400
    user = User(request.headers.get("Token"), request.headers.get("Username"))
    response = user.info_update(data)
    return jsonify(response["content"]), response["status"]
