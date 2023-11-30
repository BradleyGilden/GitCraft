#!/usr/bin/python3

"""
Configuration for environment variables for flask application

Author: Bradley Dillion Gilden
Date: 30-11-2023
"""

DATABASE_URL = ("mongodb+srv://bradleygilden:nanospartan117@cluster0."
                "kwwgi0j.mongodb.net/gitcraft?retryWrites=true&w=majority")

ICON_PACK = {
    "instagram": "https://img.icons8.com/color/48/instagram-new--v1.png",
    "facebook": "https://img.icons8.com/fluency/48/facebook-new.png",
    "linkedin": "https://img.icons8.com/color/48/linkedin.png",
    "twitter": "https://img.icons8.com/color/48/twitter--v1.png",
    "default": "https://img.icons8.com/ios/50/circled.png"
}

ICON_PACK1 = {
    "instagram": "https://img.icons8.com/ios-filled/50/instagram-new--v1.png",
    "facebook": "https://img.icons8.com/ios-filled/50/facebook-new.png",
    "linkedin": "https://img.icons8.com/ios-filled/50/linkedin.png",
    "twitter": "https://img.icons8.com/ios-filled/50/twitter.png",
    "default": "https://img.icons8.com/ios/50/circled.png"
}

ICON_PACK2 = {
    "instagram": "ri-instagram-fill",
    "facebook": "ri-facebook-circle-fill",
    "linkedin": "ri-linkedin-fill",
    "twitter": "ri-twitter-fill",
    "default": "ri-circle-fill"
}

SESSION_KEYS = {
    "login",
    "avatar",
    "name",
    "company",
    "blog",
    "location",
    "email",
    "hireable",
    "bio",
    "space_available",
    "plan",
    "following",
    "followers",
    "repo_count",
    "created_at",
    "repo_space",
    "socials",
    "streak",
    "pinned",
    "token",
    "gitcraft_user",
    "langs",
    "tools",
    "socialicons",
    "socialicons1",
    "socialicons2"
}
