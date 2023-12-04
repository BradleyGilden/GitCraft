#!/usr/bin/python3

"""
sets up the User class to handle specific request calls

Author: Bradley Dillion Gilden
Date: 11-11-2023
"""

import requests
import json
from datetime import datetime


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

    @property
    def socials(self) -> dict:
        """get's social acount information"""
        response = requests.get(f"{self.root}user/social_accounts",
                                headers=self.headers)
        return response.json()

    def info_update(self, kwargs: dict) -> dict:
        """updates user information using a patch request"""

        if kwargs:
            response = requests.patch(f"{self.root}user", headers=self.headers,
                                      data=json.dumps(kwargs))
            if response.status_code < 400:
                return {"status": response.status_code,
                        "message": "successful"}
            else:
                return {"status": response.status_code,
                        "message": "GitHub API call failed"}
        return {"status": 400, "message": "Server Error"}

    def socials_update(self, kwargs: dict) -> dict:
        """updates user information using a patch request"""

        if kwargs:
            response = requests.patch(f"{self.root}user/social_accounts",
                                      headers=self.headers,
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

        graphql_query = """
        query {
          user(login: "%s") {
            pinnedItems(first: %d, types: [REPOSITORY]) {
              nodes {
                ... on Repository {
                  name
                  description
                  url
                  primaryLanguage {
                    name
                  }
                  stargazerCount
                  forkCount
                  createdAt
                  collaborators(first: 5) {
                    nodes {
                      login
                    }
                  }
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
    def streak_stats(self):
        """gets the longest commit streak"""

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
            return User.calculate_streak_stats(response.json())
        else:
            return {}

    @staticmethod
    def calculate_streak_stats(calendar_response):
        """Uses the calendar response from longest_streak to calculate a users
        streak stats"""
        user = calendar_response.get('data', {})
        collection = user.get('user', {})
        calendar = collection.get('contributionsCollection', {})
        total = calendar.get('contributionCalendar', {})
        # get weekly data
        weeks = total.get('weeks')

        longest_streak = 0
        current_streak = 0
        # parse weekly data for daily commit data
        for week in weeks:
            for day in week['contributionDays']:
                if day['contributionCount'] > 0:
                    current_streak += 1
                else:
                    current_streak = 0

                if current_streak > longest_streak:
                    longest_streak = current_streak

        return {'longest': longest_streak,
                'current': current_streak,
                'total': total.get('totalContributions', 0)}

    @property
    def space_occupied(self):
        """total space occupied by a repository"""
        try:
            response = requests.get(f"{self.root}user/repos",
                                    headers=self.headers)
            repos = response.json()
            total = 0
            for repo in repos:
                total += repo["size"]
            return total
        except Exception:
            return 0

    @property
    def rate_limits(self):
        """get's github rate limits of a user"""
        try:
            response = requests.get(f"{self.root}rate_limit",
                                    headers=self.headers)
            jsonData = response.json()
            rest_reset = jsonData["resources"]["core"]["reset"]
            graphql_reset = jsonData["resources"]["graphql"]["reset"]
            jsonData["resources"]["core"]["reset"] = datetime.fromtimestamp(
                rest_reset
            )
            jsonData["resources"]["graphql"]["reset"] = datetime.fromtimestamp(
                graphql_reset
            )
            return {"rest": jsonData["resources"]["core"],
                    "graphql": jsonData["resources"]["graphql"]}
        except Exception:
            return {}

    def get_all_info(self):
        """this returns all infor associated with a user needed for a user
        session"""
        general = self.info
        user_document = {
            "login": general['login'],
            "avatar": general['avatar_url'],
            "name": general['name'],
            "company": general['company'],
            "blog": general['blog'],
            "location": general['location'],
            "email": general['email'],
            "hireable": general['hireable'],
            "bio": general['bio'],
            "space_available": general["plan"]["space"],
            "plan": general["plan"]["name"],
            "following": general['following'],
            "followers": general['followers'],
            "repo_count": (general['public_repos'] +
                           general['owned_private_repos']),
            "created_at": general['created_at'],
            "repo_space": self.space_occupied,
            "socials": self.socials,
            "streak": self.streak_stats,
            "pinned": self.pinned_repos(6),
            "rates": self.rate_limits
        }

        return user_document

# ************************ EXPERIMENTAL CODE ****************************

    # @property
    # def languages(self):
    #     """gets repository language stats"""
    #     graphql_query = """
    #     query {
    #       user(login: "%s") {
    #         repositories(first: 100) {
    #           nodes {
    #             name
    #             languages(first: 5) {
    #               nodes {
    #                 name
    #                 color
    #               }
    #             }
    #           }
    #         }
    #       }
    #     }
    #     """ % (self.username)
    #     response = requests.post(f"{self.root}graphql",
    #                              headers=self.graphql_headers,
    #                              data=json.dumps({"query": graphql_query}))
    #     print(response.json())
