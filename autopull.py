# Autopull
# Made by BromTeque
# Automatic git clone and pull for git repositories, to be deployed with cron.
# Make sure that the process that runs the python scrip has read and write permission to the appropriate directories.

import os
import git
import time
import github
import logging


def main():
   logging.basicConfig(
      filename = "autopull.log",
      format = "%(asctime)s %(levelname)-8s %(message)s",
      datefmt = "%Y-%m-%d %H:%M:%S",
      level = logging.ERROR
   )
   workDir = "."
   username = "BromTeque"
   user = github.Github().get_user(username)

   class Progress(git.remote.RemoteProgress):
      def update(self, op_code, cur_count, max_count = None, message = ""):
         logging.debug(self._cur_line)
   
   for starred in user.get_starred():
      logging.debug(f"Repo URL: {starred.clone_url}")
      try:
         repo = git.Repo(starred.name)
         origin = repo.remotes.origin
         try:
            for remote in repo.remotes:
               remote.fetch(progress = Progress())
            merge = repo.git.merge(f"origin/{repo.active_branch.name}")
         except git.GitCommandError as error:
            logging.error(f"Git Command error while fetching: {error}")
      except git.exc.NoSuchPathError:
         try:
            logging.debug(f"Cloning repo: {starred.name}")
            clone = git.Repo.clone_from(starred.clone_url, starred.name, progress = Progress())
         except git.GitCommandError as error:
            logging.error(f"Git Command error while cloning: {error}")


if __name__ == "__main__":
   main()