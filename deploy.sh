#!/bin/bash

# Directory where the repository is cloned
REPO_DIR="/var/www/html-project"

echo "Deploying code..."

# Check if the repository directory exists
if [ -d "$REPO_DIR" ]; then
    # Check for unstaged changes
    if [[ ! -z $(git -C "$REPO_DIR" status --porcelain) ]]; then
        echo "Unstaged changes found. Committing changes..."
        git -C "$REPO_DIR" add .
        git -C "$REPO_DIR" commit -m "Auto-commit before pull"  # Default commit message
        echo "Unstaged changes committed."
    fi

    # Attempt to pull the latest changes
    if git -C "$REPO_DIR" pull --no-rebase origin main; then
        echo "Pulled latest code from the repository."
    else
        echo "Pull failed. Attempting to resolve..."

        # Fetch the latest changes
        git -C "$REPO_DIR" fetch origin

        # Check if the current branch is ahead or behind
        LOCAL=$(git -C "$REPO_DIR" rev-parse @)
        REMOTE=$(git -C "$REPO_DIR" rev-parse @{u})

        if [ "$LOCAL" != "$REMOTE" ]; then
            echo "Local branch is behind the remote. Attempting to merge..."

            # Attempt to merge
            if git -C "$REPO_DIR" merge origin/main; then
                echo "Merge completed successfully."
            else
                echo "Merge failed. Please resolve conflicts manually."
                exit 1  # Exit if merge fails
            fi
        fi
    fi
else
    # Clone the repository if it does not exist
    git clone https://github.com/shivamsonari376/CI_CD-Project.git "$REPO_DIR"
    echo "Cloned the repository."
fi

# Restart Nginx
sudo systemctl restart nginx
echo "Nginx restarted successfully."
