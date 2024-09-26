import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the file you want to monitor
FILE_TO_WATCH = "/var/www/html-project/index.html"
REPO_DIR = "/var/www/html-project"

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == FILE_TO_WATCH:
            print(f"{FILE_TO_WATCH} has been modified. Pushing changes to GitHub...")
            push_changes()

def push_changes():
    # Define the bash command to add, commit, and push changes directly in Python
    bash_command = f"""
    cd {REPO_DIR}
    git add index.html
    git commit -m "Auto-update index.html"
    git push origin main
    """
    process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE)
    process.communicate()

if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FILE_TO_WATCH), recursive=False)

    print(f"Monitoring changes to {FILE_TO_WATCH}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

