#! /usr/bin/python3
import os
import subprocess

def pull_repos(root_dir="pkg"):
    """Attempt to pull latest changes for all repos."""
    success = []
    attention = []

    for repo in os.listdir(root_dir):
        repo_path = os.path.join(root_dir, repo)
        git_dir = os.path.join(repo_path, ".git")

        if not os.path.isdir(git_dir):
            continue  # skip non-git dirs

        try:
            subprocess.run(
                ["git", "-C", repo_path, "pull", "--ff-only"],
                capture_output=True,
                text=True,
                check=True
            )
            success.append(repo)
        except subprocess.CalledProcessError:
            attention.append(repo)

    print("\nThese repositories updated successfully:")
    if success:
        for repo in success:
            print(f"  - {repo}")
    else:
        print("  (none)")

    print("\nThese repositories appear to need attention:")
    if attention:
        for repo in attention:
            print(f"  - {repo}")
    else:
        print("  (none)")


if __name__ == "__main__":
    # Step 2: try pulling latest changes
    pull_repos("pkg")
