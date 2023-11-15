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
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "GitCraft-API/v1"
        }
        self.graphql_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "GitCraft-API/v1"
        }
        self.username = username
        self.root = "https://api.github.com/"

    @property
    def info(self) -> dict:
        """collects basic information of a user"""
        response = requests.get(f"{self.root}user", headers=self.headers)
        return response.json()

    def info_update(self, **kwargs):
        """updates user information using a patch request"""
        import json

        if kwargs:
            response = requests.patch(f"{self.root}user", headers=self.headers,
                                      data=json.dumps(kwargs))
            return {"status": response.status_code, "content": response.json()}
        return {"status": 400, "content": {"message": "default error"}}

    @property
    def test_credentials(self) -> int:
        """tests a users credentials"""
        response = requests.get(f"{self.root}user", headers=self.headers)
        return response.status_code

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

    def pinned_repos(self, num: int) -> dict:
        """get list of pinned repositories and their repsective info"""
        import json

        graphql_query = """
        query {
          user(login: "%s") {
            pinnedItems(first: %d, types: [REPOSITORY]) {
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
        """ % (self.username, num)

        try:
            response = requests.post(f"{self.root}graphql",
                                     headers=self.graphql_headers,
                                     data=json.dumps({"query": graphql_query}))

            return response.json()['data']['user']['pinnedItems']['nodes']
        except Exception:
            return {}

    @property
    def longest_streak(self):
        """gets longest commit streak"""
        import json

        # Your GraphQL query for contributions
        query = """
        {
        user(login: "%s") {
            contributionsCollection {
            contributionCalendar {
                totalContributions
                weeks {
                contributionDays {
                    contributionCount
                    date
                }
                }
            }
            }
        }
        }
        """ % self.username

        response = requests.post(f"{self.root}graphql",
                                 data=json.dumps({'query': query}),
                                 headers=self.graphql_headers)
        if response.status_code == 200:
            return User.calculate_longest_streak(response.json())
        else:
            return {}

    @staticmethod
    def calculate_longest_streak(calendar_response):
        user = calendar_response.get('data', {})
        collection = user.get('user', {})
        calendar = collection.get('contributionsCollection', {})
        total = calendar.get('contributionCalendar', {})
        weeks = total.get('weeks')

        longest_streak = 0
        current_streak = 0
        for week in weeks:
            for day in week['contributionDays']:
                if day['contributionCount'] > 0:
                    current_streak += 1
                else:
                    current_streak = 0

                if current_streak > longest_streak:
                    longest_streak = current_streak

        return {'longest': longest_streak, 'current': current_streak}

    # def get_all_info(self):
    #     """this returns all infor associated with a user needed for a user
    #     session"""

    #     user_document = {
    #         "general": self.info
    #     }
