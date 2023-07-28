# Autopull v1.0
# Made by BromTeque


import sys
import logging
import argparse
import github
import git


def main(username=None, debug=False):
    """Main function"""

    logging.basicConfig(
        filename="autopull.log",
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO
    )

    if username is None:
        logging.error("No username was provided. Exiting...")
        sys.exit(1)

    user = github.Github().get_user(username)

    class Progress(git.remote.RemoteProgress):
        """Print progress"""

        def update(self, op_code, cur_count, max_count=None, message=""):
            logging.debug(self._cur_line)

    for starred in user.get_starred():
        logging.info("Updating Repo: %s", starred.full_name)
        try:
            repo = git.Repo(starred.name)
            try:
                logging.debug("Fetching repo: %s", starred.name)
                for remote in repo.remotes:
                    remote.fetch(progress=Progress())
                logging.debug("Merging(/Pulling) repo: %s", starred.name)
                repo.git.merge(f"origin/{repo.active_branch.name}")
            except git.GitCommandError as error:
                logging.error("Git Command error while fetching: %s", error)
            except git.exc.BadName as error:
                logging.error("Invalid branch name while merging: %s", error)
        except git.exc.NoSuchPathError:
            try:
                logging.debug("Cloning repo: %s", starred.name)
                git.Repo.clone_from(
                    starred.clone_url,
                    starred.name,
                    progress=Progress()
                )
            except git.GitCommandError as error:
                logging.error("Git Command error while cloning: %s", error)

    logging.debug("End of Script")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="autopull")
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "-u", "--username",
        type=str,
        help="Specify a username"
    )
    args = parser.parse_args()

    main(args.username, debug=args.debug)
