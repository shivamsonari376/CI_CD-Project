import requests
import os

# GitHub repo details
GITHUB_REPO = "shivamsonari376/CI_CD-Project"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Path to store the last commit hash
COMMIT_HASH_FILE = "/var/www/html-project/last_commit.txt"

def get_latest_commit():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    # Print the status code and response text for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        return response.json()[0]['sha']
    else:
        raise Exception("Failed to fetch the latest commits.")


def get_last_commit():
    if os.path.exists(COMMIT_HASH_FILE):
        with open(COMMIT_HASH_FILE, 'r') as file:
            return file.read().strip()
    return None

def update_last_commit(commit_hash):
    with open(COMMIT_HASH_FILE, 'w') as file:
        file.write(commit_hash)

def check_for_new_commit():
    latest_commit = get_latest_commit()
    last_commit = get_last_commit()

    if latest_commit != last_commit:
        print("New commit found. Deploying...")
        update_last_commit(latest_commit)
        os.system("/var/www/html-project/deploy.sh")
    else:
        print("No new commits.")

if __name__ == "__main__":
    check_for_new_commit()
