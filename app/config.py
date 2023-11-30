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
    "reddit": "https://img.icons8.com/doodle/48/reddit--v4.png",
    "telegram": "https://img.icons8.com/color/48/telegram-app.png",
    "discord": "https://img.icons8.com/color/48/discord-logo.png",
    "snapchat": "https://img.icons8.com/doodle/48/snapchat.png",
    "default": "https://img.icons8.com/ios/50/circled.png"
}

ICON_PACK1 = {
    "instagram": "https://img.icons8.com/ios-filled/50/instagram-new--v1.png",
    "facebook": "https://img.icons8.com/ios-filled/50/facebook-new.png",
    "linkedin": "https://img.icons8.com/ios-filled/50/linkedin.png",
    "twitter": "https://img.icons8.com/ios-filled/50/twitter.png",
    "reddit": "https://img.icons8.com/ios-filled/50/reddit--v1.png",
    "telegram": "https://img.icons8.com/ios-filled/50/telegram-app.png",
    "discord": "https://img.icons8.com/ios-filled/50/discord-logo.png",
    "snapchat": "https://img.icons8.com/ios-filled/50/snapchat--v1.png",
    "default": "https://img.icons8.com/ios/50/circled.png"
}

ICON_PACK2 = {
    "instagram": "ri-instagram-fill",
    "facebook": "ri-facebook-circle-fill",
    "linkedin": "ri-linkedin-fill",
    "twitter": "ri-twitter-fill",
    "reddit": "ri-reddit-fill",
    "telegram": "ri-telegram-fill",
    "discord": "ri-discord-fill",
    "snapchat": "ri-snapchat-fill",
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
