from github import Github

g = Github("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")

user = g.get_user()

print(user.login)
print(user.total_private_repos)
print(user.avatar_url)
print(user.followers)
print(user.url)

g.close()
