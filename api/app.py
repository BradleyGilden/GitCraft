#!/usr/bin/python3

"""
This is the root endpoint for flask to serve files

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""
from flask import Flask, make_response, render_template  # noqa
from flask_cors import CORS


app = Flask(__name__, template_folder="../web/html")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    """returns the index page of the project"""
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    """returns custom template for page not found"""
    return make_response(render_template('404.html'), 404)


if __name__ == '__main__':
    # runs application in debug mode for testing on port 5500
    app.run(host='0.0.0.0', port=5500, debug=True, threaded=True)
