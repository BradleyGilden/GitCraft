from github import Github
import requests
import json
from sys import argv

# Authentication is defined via github.Auth
from github import Auth

# using an access token
token = argv[1]
auth = Auth.Token(f"{token}")

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)

user = g.get_user()
total_commits = 0

# Loop through the user's repositories and count the commits
print(user.bio)
print(user.login)
print(user.total_private_repos)
print(user.avatar_url)
print(user.followers)
print(user.url)

g.close()

def get_total_commits_from_user(username):
    # Replace "YOUR_ACCESS_TOKEN" with your personal access token
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
               }

    # Construct the search query
    query = f"committer:{username}"

    # Send the GET request to the `search/commits` endpoint
    response = requests.get("https://api.github.com/search/commits", headers=headers, params={"q": query})

    # Check for successful response
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract the total number of commits
        total_commits = data["total_count"]

        return total_commits
    else:
        print(f"Error: Failed to fetch commits: {response.status_code}")
        return None

# Get total commits for a specific user
total_commits = get_total_commits_from_user("BradleyGilden")
print("Total commits for user:", total_commits)
