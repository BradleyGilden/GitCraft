#!/usr/bin/python3

"""
This is the root endpoint for flask to serve files

Author: Bradley Dillion Gilden
Date: 12-11-2023
"""
from flask import Flask, make_response, render_template
from flask_cors import CORS
from api.blueprints.api_blueprint import api_bp

app = Flask(__name__, template_folder="../web/html")

# Registering blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Enabling CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", strict_slashes=False)
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
