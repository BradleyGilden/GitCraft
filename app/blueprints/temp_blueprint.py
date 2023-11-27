#!/usr/bin/python3

"""
This blue print manages the download and viewing of templates

Author: Bradley Dillion Gilden
Date: 24-11-2023
"""

from flask import (Blueprint, render_template,
                   session, current_app, make_response)
import zipfile
from io import BytesIO
tmp_bp = Blueprint('tmp', __name__)


@tmp_bp.route("/vporfolio", strict_slashes=False)
def view_portfolio():
    """allows the user to dynamically view the downloaded portfolio"""
    socialicons = {
        "instagram": "https://img.icons8.com/ios/50/instagram-new--v1.png",
        "facebook": "https://img.icons8.com/ios/50/facebook-new.png",
        "linkedin": "https://img.icons8.com/ios/50/linkedin.png",
        "twitter": "https://img.icons8.com/ios/50/twitter--v1.png",
        "reddit": "https://img.icons8.com/ios/50/reddit--v1.png",
        "telegram": "https://img.icons8.com/ios/50/telegram.png",
        "discord": "https://img.icons8.com/ios/50/discord-logo--v1.png",
        "snapchat": "https://img.icons8.com/ios/50/snapchat--v1.png",
        "default": "https://img.icons8.com/ios/50/circled.png"
    }
    tools = [tool.split("|")[2] for tool in session["tools"]]
    langs = [lang.split("|")[2] for lang in session["langs"]]
    return render_template("portfolio.html", **session, toolimgs=tools,
                           langimgs=langs, socialicons=socialicons,
                           downloadable=False)


@tmp_bp.route("/dporfolio", strict_slashes=False)
def download_portfolio():
    """downloads the portfolio that was dynamically created"""
    socialicons = {
        "instagram": "https://img.icons8.com/ios/50/instagram-new--v1.png",
        "facebook": "https://img.icons8.com/ios/50/facebook-new.png",
        "linkedin": "https://img.icons8.com/ios/50/linkedin.png",
        "twitter": "https://img.icons8.com/ios/50/twitter--v1.png",
        "reddit": "https://img.icons8.com/ios/50/reddit--v1.png",
        "telegram": "https://img.icons8.com/ios/50/telegram.png",
        "discord": "https://img.icons8.com/ios/50/discord-logo--v1.png",
        "snapchat": "https://img.icons8.com/ios/50/snapchat--v1.png",
        "default": "https://img.icons8.com/ios/50/circled.png"
    }
    tools = [tool.split("|")[2] for tool in session["tools"]]
    langs = [lang.split("|")[2] for lang in session["langs"]]

    css_file_path = '/static/css/portfolio.css'
    html_content = render_template("portfolio.html", **session, toolimgs=tools,
                                   langimgs=langs, socialicons=socialicons,
                                   downloadable=True)
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
