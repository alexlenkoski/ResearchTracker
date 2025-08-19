#!  /home/alex/miniforge3/envs/pytorch_env/bin/python
import os
import subprocess
from pathlib import Path

PKG_DIR = Path.home() / "pkg"

import os
import subprocess

def check_uncommitted_repos(root_dir=PKG_DIR):
    """Check which repos have uncommitted changes (modified/untracked files)."""
    clean = []
    dirty = []

    all_repos = os.listdir(root_dir)
    for i in range(len(all_repos)):
        repo = all_repos[i]
        repo_path = os.path.join(root_dir, repo)

        result = subprocess.run(
            ["git", "-C", repo_path, "status", "--porcelain"],
            capture_output = True,
            text = True,
            check = True
        )
        status = result.stdout.strip()
        
        if status:  # any output means uncommitted changes
            dirty.append(repo)
        else:
            clean.append(repo)

    if dirty:
        print("Commit These:")
        for repo in dirty:
            print(f"  - {repo}")
    else:
        print("You good bro")

if __name__ == "__main__":
    check_uncommitted_repos()
