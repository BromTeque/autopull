# Autopull v1.1
# Made by BromTeque
# Automatic git clone and pull for git repositories, to be deployed with cron.
# Make sure that the process that runs the python scrip has read and write permission to the appropriate directories.


import git
import github
import logging
import argparse


# Global Variables
USERNAME = "BromTeque"


def main(debug = False):
   logging.basicConfig(
      filename = "autopull.log",
      format = "%(asctime)s %(levelname)-8s %(message)s",
      datefmt = "%Y-%m-%d %H:%M:%S",
      level = logging.DEBUG if debug else logging.INFO
   )
   user = github.Github().get_user(USERNAME)

   class Progress(git.remote.RemoteProgress):
      def update(self, op_code, cur_count, max_count = None, message = ""):
         if debug:
            logging.debug(self._cur_line)
   
   for starred in user.get_starred():
      logging.info(f"Updating Repo: {starred.full_name}")
      try:
         repo = git.Repo(starred.name)
         repo.remotes.origin
         try:
            logging.debug(f"Fetching repo: {starred.name}")
            for remote in repo.remotes:
               remote.fetch(progress = Progress())
            logging.debug(f"Merging(/Pulling) repo: {starred.name}")
            repo.git.merge(f"origin/{repo.active_branch.name}")
         except git.GitCommandError as error:
            logging.error(f"Git Command error while fetching: {error}")
      except git.exc.NoSuchPathError:
         try:
            logging.debug(f"Cloning repo: {starred.name}")
            git.Repo.clone_from(starred.clone_url, starred.name, progress = Progress())
         except git.GitCommandError as error:
            logging.error(f"Git Command error while cloning: {error}")


if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "autopull")
   parser.add_argument("-d", "--debug", action = "store_true", help = "Enable debug mode")

   args = parser.parse_args()

   main(debug = args.debug)