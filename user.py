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
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.graphql_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.username = username
        self.root = "https://api.github.com/"

    @property
    def user_info(self) -> dict:
        """collects basic information of a user"""
        response = requests.get(f"{self.root}user", headers=self.headers)
        return response.json()

    def user_info_update(self, **kwargs):
        """updates user information using a patch request"""
        import json

        if kwargs:
            response = requests.patch(f"{self.root}user", headers=self.headers,
                                      data=json.dumps(kwargs))
            return {"status": response.status_code, "content": response.json()}
        return {"status": 404, "conetent": {"message": "default"}}

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
        try:
            response = requests.get(f"{self.root}search/commits",
                                    headers=self.headers,
                                    params={"q": f"author:{self.username}"})

            return response.json()["total_count"]
        except Exception:
            return {}

    @property
    def pinned_repos(self) -> int:
        """get list of pinned repositories and their repsective info"""
        import json

        graphql_query = """
        query {
          user(login: "%s") {
            pinnedItems(first: 6, types: [REPOSITORY]) {
              nodes {
                ... on Repository {
                  name
                  description
                  url
                }
              }
            }
          }
        }
        """ % self.username

        try:
            response = requests.post(f"{self.root}graphql", 
                                     headers=self.graphql_headers, 
                                     data=json.dumps({"query": graphql_query}))

            return response.json()['data']['user']['pinnedItems']['nodes']
        except Exception:
            return {}
