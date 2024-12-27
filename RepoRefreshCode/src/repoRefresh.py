import os
import git
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Replace these with values from your .env file
GITHUB_URL = os.getenv("GITHUB_URL")
BRANCH = os.getenv("BRANCH")
LOCAL_REPO_PATH = os.getenv("LOCAL_REPO_PATH")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def set_git_identity():
    """Set Git user name and email for commits."""
    os.system('git config --global user.name "Nisal Herath"')
    os.system('git config --global user.email "anushkanisalherath@gmail.com"')


def clone_or_initialize_repo():
    """Clone the repository if not already cloned."""
    if not os.path.exists(LOCAL_REPO_PATH):
        print("Cloning the repository from GitHub...")
        try:
            repo = git.Repo.clone_from(
                f"https://{GITHUB_TOKEN}@{GITHUB_URL[len('https://'):]}",
                LOCAL_REPO_PATH,
                branch=BRANCH
            )
            print("Repository cloned successfully.")
        except Exception as e:
            print(f"Error while cloning repository: {e}")
            raise
    else:
        print("Repository already exists locally. Pulling latest changes...")
        try:
            repo = git.Repo(LOCAL_REPO_PATH)
            repo.remotes.origin.pull()
            print("Pulled latest changes successfully.")
        except Exception as e:
            print(f"Error while pulling repository: {e}")
            raise
    return repo


def modify_readme():
    """Add a character to the README file."""
    readme_path = os.path.join(LOCAL_REPO_PATH, "README.md")
    try:
        if not os.path.exists(readme_path):
            print("README.md does not exist. Creating a new README.md...")
            with open(readme_path, "w") as file:
                file.write("# My GitHub Activity\n")
                print("README.md created.")
        else:
            print("README.md exists. Modifying it...")

        with open(readme_path, "a") as file:
            file.write("A")  # Append a character to the README file
        print(f"README.md updated at {datetime.now()}")
    except Exception as e:
        print(f"Error while modifying README.md: {e}")
        raise


def push_changes(repo):
    """Commit and push changes to GitHub."""
    try:
        print("Staging changes...")
        repo.git.add("README.md")
        print("Committing changes...")
        repo.git.commit("-m", f"Update README at {datetime.now()}")
        print("Pushing changes to GitHub...")
        repo.remotes.origin.push()
        print("Changes pushed successfully.")
    except Exception as e:
        print(f"Error while pushing changes: {e}")
        raise


def job():
    """Perform the scheduled job."""
    print(f"\n--- Job started at {datetime.now()} ---")
    try:
        set_git_identity()  # Set Git identity before repo operations
        repo = clone_or_initialize_repo()
        modify_readme()
        push_changes(repo)
        print(f"--- Job completed successfully at {datetime.now()} ---\n")
    except Exception as e:
        print(f"--- Job failed: {e} ---\n")


# Schedule the task to run every hour at the 0th minute
schedule.every().hour.at(":00").do(job)


def restart_script():
    """Restarts the script if it fails or is closed unexpectedly."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def run_scheduler():
    """Run the scheduled job indefinitely."""
    print("Scheduler started. Waiting for the next scheduled task...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(10)  # Sleep for 10 seconds before checking again
        except Exception as e:
            print(f"Error encountered: {e}")
            restart_script()  # Restart the script if any error occurs


if __name__ == "__main__":
    # Directly start the scheduler without checking for the first run
    try:
        run_scheduler()
    except Exception as e:
        print(f"Error encountered in main script: {e}")
        restart_script()  # Restart the script if the main function crashes
