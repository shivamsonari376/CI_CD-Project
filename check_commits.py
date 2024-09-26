import requests
import os
import subprocess

# GitHub repo details
GITHUB_REPO = "shivamsonari376/CI_CD-Project"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Path to store the last commit hash
COMMIT_HASH_FILE = "/var/www/html-project/last_commit.txt"
REPO_DIR = "/var/www/html-project"

def get_latest_commit():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()[0]['sha']
    else:
        print(f"Failed to fetch the latest commits. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        raise Exception("Error fetching commits.")

def get_last_commit():
    if os.path.exists(COMMIT_HASH_FILE):
        with open(COMMIT_HASH_FILE, 'r') as file:
            return file.read().strip()
    return None

def update_last_commit(commit_hash):
    with open(COMMIT_HASH_FILE, 'w') as file:
        file.write(commit_hash)

def deploy_code():
    print("Deploying code...")

    try:
        # Clone or pull the latest code
        if os.path.exists(REPO_DIR):
            # Check for unstaged changes
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=REPO_DIR
            ).decode().strip()

            if status_output:  # If there are unstaged changes
                print("Unstaged changes found. Committing changes...")
                os.system(f"cd {REPO_DIR} && git add .")
                os.system(f"cd {REPO_DIR} && git commit -m 'Auto-commit before pull'")  # Default commit message
                print("Unstaged changes committed.")

            # Pull latest changes with merge
            os.system(f"cd {REPO_DIR} && git pull --no-rebase origin main")
            print("Pulled latest code from the repository.")
        else:
            os.system(f"git clone https://github.com/{GITHUB_REPO}.git {REPO_DIR}")
            print("Cloned the repository.")

        # Restart Nginx (adjust this command if necessary)
        os.system("sudo systemctl restart nginx")
        print("Nginx restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during deployment: {e.output.decode()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def check_for_new_commit():
    latest_commit = get_latest_commit()
    last_commit = get_last_commit()

    if latest_commit != last_commit:
        print("New commit found. Deploying...")
        update_last_commit(latest_commit)
        deploy_code()
    else:
        print("No new commits.")

if __name__ == "__main__":
    check_for_new_commit()
