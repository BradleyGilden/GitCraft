#!/usr/bin/python3

"""
This blue print manages the download and viewing of templates

Author: Bradley Dillion Gilden
Date: 24-11-2023
"""

from flask import (Blueprint, render_template, request,  # noqa
                   session, current_app, make_response)
import zipfile
from io import BytesIO
tmp_bp = Blueprint('tmp', __name__)


@tmp_bp.route("/vporfolio", strict_slashes=False)
def view_portfolio():
    """allows the user to dynamically view the downloaded portfolio"""
    tools = [tool.split("|")[2] for tool in session["tools"]]
    langs = [lang.split("|")[2] for lang in session["langs"]]
    return render_template("portfolio.html", **session, toolimgs=tools,
                           langimgs=langs, downloadable=False)


@tmp_bp.route("/dporfolio", strict_slashes=False)
def download_portfolio():
    """downloads the portfolio that was dynamically created"""
    tools = [tool.split("|")[2] for tool in session["tools"]]
    langs = [lang.split("|")[2] for lang in session["langs"]]

    css_file_path = '/static/css/portfolio.css'
    html_content = render_template("portfolio.html", **session, toolimgs=tools,
                                   langimgs=langs, downloadable=True)
    css_content = open(current_app.root_path +
                       css_file_path).read()
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a',
                         zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('portfolio.html', html_content)
        zip_file.writestr('portfolio.css', css_content)

    zip_buffer.seek(0)
    response = make_response(zip_buffer.read())
    attatch_header = "attachment; filename=portfolio.zip"
    response.headers["Content-Disposition"] = attatch_header
    response.headers["Content-Type"] = "application/zip"
    return response


@tmp_bp.route("/vscrollable", strict_slashes=False)
def view_portfolio_scrollable():
    """allows the user to dynamically view the downloaded portfolio"""
    tools = [tool.split("|")[2] for tool in session["tools"]]
    langs = [lang.split("|")[2] for lang in session["langs"]]
    return render_template("portfolio_scrollable.html", **session,
                           toolimgs=tools, langimgs=langs, downloadable=False,
                           occupation=request.args.get('param1'))


@tmp_bp.route("/dscrollable", strict_slashes=False)
def download_portfolio_scrollable():
    """downloads the portfolio that was dynamically created"""
    tools = [tool.split("|")[2] for tool in session["tools"]]
    langs = [lang.split("|")[2] for lang in session["langs"]]

    css_file_path = '/static/css/portfolio_scrollable.css'
    html_content = render_template("portfolio_scrollable.html", **session,
                                   toolimgs=tools, langimgs=langs,
                                   downloadable=True,
                                   occupation=request.args.get('param1'))
    css_content = open(current_app.root_path +
                       css_file_path).read()
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a',
                         zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('portfolio_scrollable.html', html_content)
        zip_file.writestr('portfolio_scrollable.css', css_content)

    zip_buffer.seek(0)
    response = make_response(zip_buffer.read())
    attatch_header = "attachment; filename=portfolio_scrollable.zip"
    response.headers["Content-Disposition"] = attatch_header
    response.headers["Content-Type"] = "application/zip"
    return response
