#!/bin/bash

# Path to deploy the project
PROJECT_DIR="/var/www/html-project"

# Clone or pull the latest changes from GitHub
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "Pulling latest changes..."
    git -C "$PROJECT_DIR" pull
else
    echo "Cloning the repository..."
    git clone https://github.com/shivamsonari376/CI_CD-Project "$PROJECT_DIR"
fi

# Reload Nginx to apply any changes
echo "Restarting Nginx..."
sudo systemctl reload nginx
echo "Deployment complete."
