#!/usr/bin/env python3
import subprocess
from pathlib import Path

PKG_DIR = Path.home() / "pkg"

def is_git_repo(path):
    return (path / ".git").is_dir()

def try_git_pull(repo_path):
    """Attempts git pull. Returns (success, message)."""
    try:
        # Run git pull
        output = subprocess.check_output(
            ["git", "pull", "--no-rebase"],
            cwd=repo_path,
            stderr=subprocess.STDOUT,
            text=True
        )
        return True, output
    except subprocess.CalledProcessError as e:
        # If pull fails, check if it mentions conflicts
        if "CONFLICT" in e.output or "merge" in e.output.lower():
            return False, "Merge conflict detected, manual intervention required."
        else:
            return False, f"Pull failed for another reason:\n{e.output}"

def main():
    for repo in PKG_DIR.iterdir():
        if is_git_repo(repo):
            success, message = try_git_pull(repo)
            if success:
                print(f"{repo.name}: Successfully updated.")
            else:
                print(f"{repo.name}: {message}")

if __name__ == "__main__":
    main()
