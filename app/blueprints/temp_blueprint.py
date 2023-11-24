#!/usr/bin/python3

"""
This blue print manages the download and viewing of templates

Author: Bradley Dillion Gilden
Date: 24-11-2023
"""

from flask import (Blueprint, render_template, jsonify, request,  # noqa
                   session, current_app, make_response)
import zipfile
from io import BytesIO
tmp_bp = Blueprint('tmp', __name__)


@tmp_bp.route("/vporfolio", strict_slashes=False)
def view_portfolio():
    """allows the user to dynamically view the downloaded portfolio"""
    return render_template("portfolio.html", **session)


@tmp_bp.route("/dporfolio", strict_slashes=False)
def download_portfolio():
    """downloads the portfolio that was dynamically created"""
    css_file_path = '/static/css/portfolio.css'
    html_content = render_template("portfolio.html", **session)
    css_content = open(current_app.root_path +
                       css_file_path).read()
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a',
                         zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('portfolio.html', html_content)
        zip_file.writestr('styling.css', css_content)

    zip_buffer.seek(0)
    response = make_response(zip_buffer.read())
    attach_header = "attachment; filename=downloaded_files.zip"
    response.headers["Content-Disposition"] = attach_header
    response.headers["Content-Type"] = "application/zip"
    return response
