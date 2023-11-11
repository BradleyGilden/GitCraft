#!/usr/bin/python3

"""
used to test custom classes

Author: Bradley Dillion Gilden
Date: 11-11-2023
"""


from user import User
from sys import argv


if __name__ == '__main__':
    token = argv[1]
    username = "BradleyGilden"

    user = User(token, username)

    print(user.pinned_repos)
