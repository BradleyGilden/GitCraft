#!/usr/bin/python3

"""
sets up the User class to handle specific request calls

Author: Bradley Dillion Gilden
Date: 11-11-2023
"""

import requests


class User:
    def __init__(self, token: str, username: str):
        """sets up variables to make queries"""
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.username = username
        self.root = "https://api.github.com/"

    @property
    def user_info(self) -> dict:
        """collects basic information of a user"""
        response = requests.get(f"{self.root}user", headers=self.headers)
        return response.json()

    @property
    def test_credentials(self) -> bool:
        """tests a users credentials"""
        response = self.user_info
        login = response.get("login")
        if login is not None and login == self.username:
            return True
        else:
            return False

    @property
    def num_commits(self) -> int:
        """calculates number of commits generated from a user"""
        response = requests.get(f"{self.root}search/commits",
                                headers=self.headers,
                                params={"q": f"author:{self.username}"})

        return response.json()["total_count"]
