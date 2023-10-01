#!/usr/bin/env python3

import sys
import subprocess

def git_commit_push(message):
    # Run 'git add .'
    subprocess.run(["git", "add", "."], check=True)

    # Run 'git commit -m "message"'
    subprocess.run(["git", "commit", "-m", message], check=True)

    # Run 'git push'
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a commit message.")
        sys.exit(1)

    commit_message = sys.argv[1]
    git_commit_push(commit_message)
