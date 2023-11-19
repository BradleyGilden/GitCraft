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
from secrets import token_hex

app = Flask(__name__)
app.secret_key = token_hex(16)

# establishing mongodb connection
connection_str = ("mongodb+srv://bradleygilden:nanospartan117@cluster0."
                  "kwwgi0j.mongodb.net/gitcraft?retryWrites=true&w=majority")
app.config['MONGO_URI'] = connection_str
mongo.init_app(app)

# Registering blueprints
app.register_blueprint(db_bp, url_prefix='/db')
app.register_blueprint(api_bp, url_prefix='/api')

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
    """returns the index page of the project"""
    if 'login' in session:
        return render_template("dashboard.html", **session)
    else:
        return render_template("authentication.html")


@app.errorhandler(404)
def page_not_found(error):
    """returns custom template for page not found"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    # runs application in debug mode for testing on port 5500
    app.run(host='0.0.0.0', port=5500, debug=True, threaded=True)
