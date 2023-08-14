#    Autopull - A simple script that automatically pulls or clones GitHub repositores.
#
#    Copyright (C) 2023  BromTeque
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Contact: autopull (ætt) bromteque (dot) com


"""Module exit used to cancel script on error"""
import sys

import logging
import logging.handlers
import argparse
import github
import git


VERSION = "0.0.1"


def main(username=None, debug=False):
    """Main function"""

    # Logging
    logger = logging.getLogger("AutpullLogger")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler = logging.handlers.RotatingFileHandler(
        "autopull.log",
        maxBytes=1000000,
        backupCount=10
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Check username variable
    if username is None:
        print('Username argument is required.')
        print('Usage: ./autopull -u <GitHub username>')
        print('You can also use --username instead of -u.')
        logger.error("No username was provided. Exiting...")
        sys.exit(1)

    # Do GitHub API call
    user = github.Github().get_user(username)

    class Progress(git.remote.RemoteProgress):
        """Print progress"""

        def update(self, op_code, cur_count, max_count=None, message=""):
            logger.debug(self._cur_line)

    # Clone or pull repository
    for starred in user.get_starred():
        logger.info("Updating Repo: %s", starred.full_name)
        try:
            repo = git.Repo(starred.name)
            try:
                logger.debug("Fetching repo: %s", starred.name)
                for remote in repo.remotes:
                    remote.fetch(progress=Progress())
                logger.debug("Merging(/Pulling) repo: %s", starred.name)
                repo.git.merge(
                    f"origin/{repo.active_branch.name}",
                    progress=Progress()
                )
            except git.GitCommandError as error:
                logger.error("Git Command error while fetching: %s", error)
            except git.exc.BadName as error:
                logger.error("Invalid branch name while merging: %s", error)
        except git.exc.NoSuchPathError:
            try:
                logger.debug("Cloning repo: %s", starred.name)
                git.Repo.clone_from(
                    starred.clone_url,
                    starred.name,
                    progress=Progress()
                )
            except git.GitCommandError as error:
                logger.error("Git Command error while cloning: %s", error)
        except git.GitCommandError as error:
            logger.error("Git command error while fetching: %s", error)

    logger.debug("End of Script")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="autopull")
    parser.add_argument(
        "-u", "--username",
        type=str,
        help="Specify a GitHub USERNAME"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    args = parser.parse_args()

    main(username=args.username, debug=args.debug)
