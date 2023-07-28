# Autopull
# Made by BromTeque


import sys
import logging
import logging.handlers
import argparse
import github
import git


VERSION = "1.0.0"


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
        help="Specify a username"
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
