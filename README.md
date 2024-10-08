# CI_CD-Project
Description
Create a complete CI-CD pipeline using bash, python, and crontabs. The list of tasks is specified below: 

Task 1: Set Up a Simple HTML Project 
Create a simple HTML project and push it to a GitHub repository. 
Task 2: Set Up an AWS EC2/Local Linux Instance with Nginx
Task 3: Write a Python Script to Check for New Commits
 Create a Python script to check for new commits using the GitHub API.
Task 4: Write a Bash Script to Deploy the Code
Create a bash script to clone the latest code and restart Nginx.
Task 5: Set Up a Cron Job to Run the Python Script
Create a cron job to run the Python script at regular intervals.
Task 6: Test the Setup 
Make a new commit to the GitHub repository and check that the changes are automatically deployed. 



Solution:
Create the Python script (check_commits.py): This script uses the GitHub API to check for new commits.
Create the Bash deploy script (deploy.sh). This script will be used for cloning and pulling the repositiory.It also includes the following functionality>

      Error Handling on Pull:

           The script now checks if the git pull command fails. If it does, it attempts to fetch the latest changes and 
           check the state of the local and remote branches.
      Merging:

           If the local branch is behind, it will attempt to merge the remote branch into the local one. If there are 
           conflicts during the merge, the script will exit and prompt the user to resolve them manually.

Add the cron job to run the Python script every minute (or adjust as needed):

Create the Python script(watch_changes.py)- to monitor the index.html file for any changes from local system.Once a change is detected, the script should automatically commit and push the changes to your GitHub repository.
