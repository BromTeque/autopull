import github

username = "BromTeque"

user = github.Github().get_user(username)

for repo in user.get_starred():
   print(repo.clone_url)