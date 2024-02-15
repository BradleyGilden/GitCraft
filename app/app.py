#!/usr/bin/python3

"""
This is the root endpoint for flask to serve files

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""
from flask import Flask, render_template, session
from flask_cors import CORS
from app.blueprints.api_blueprint import api_bp
from app.blueprints.db_blueprint import db_bp, mongo
from app.blueprints.temp_blueprint import tmp_bp
from secrets import token_hex
from os import getenv
from datetime import timedelta

app = Flask(__name__)
app.secret_key = token_hex(16)

# allowing all successful logins to have an open session of 24 hours
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initializing mongodb connection in flask
app.config['MONGO_URI'] = getenv("DB_URL")
mongo.init_app(app)

# Registering blueprints
app.register_blueprint(db_bp, url_prefix='/db')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(tmp_bp, url_prefix='/tmp')

# Enabling CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", strict_slashes=False)
def index():
    """returns the index page of the project"""
    return render_template("index.html")


@app.route("/authentication", strict_slashes=False)
def authentication():
    """returns the login/signup of the project"""
    if 'login' in session:
        return render_template("dashboard.html", **session)
    else:
        return render_template("authentication.html")


@app.route("/dashboard", strict_slashes=False)
def dashboard():
    """returns the dashboard page of the project"""
    if 'login' in session:
        return render_template("dashboard.html", **session)
    else:
        return render_template("authentication.html")


@app.route("/temps", strict_slashes=False)
def temps():
    """returns the templates page of the project"""
    if 'login' in session:
        return render_template("temps.html", **session)
    else:
        return render_template("authentication.html")


@app.route("/settings", strict_slashes=False)
def settings():
    """returns the settings page of the project"""
    if 'login' in session:
        return render_template("settings.html", **session)
    else:
        return render_template("authentication.html")


@app.errorhandler(404)
def page_not_found(error):
    """returns custom template for page not found"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    # runs application in debug mode for testing on port 5500
    app.run(host='0.0.0.0', port=5500, debug=True, threaded=True)
