#! /home/alex/miniforge3/envs/pytorch_env/bin/python

import argparse
import os
import sys
from git import Repo, InvalidGitRepositoryError
from datetime import datetime, date

def get_target_date():
    if len(sys.argv) > 1:
        try:
            return datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    return date.today()

def count_changes_in_repo(repo_path,
                          target_date,
                          author_name,
                          excluded_message):
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        return 0

    total_insertions = 0
    total_deletions = 0

    for commit in repo.iter_commits():
        commit_date = datetime.fromtimestamp(commit.committed_date).date()
        right_date = (commit_date == target_date)
        right_author = (author_name == commit.author.name)
        not_cleaning = commit.message.strip() != excluded_message
        if (right_date and right_author and not_cleaning):
            stats = commit.stats.total
            total_insertions += stats.get('insertions', 0)
            total_deletions += stats.get('deletions', 0)

    return total_insertions + total_deletions

def find_git_repos(base_path):
    git_repos = []
    for root, dirs, files in os.walk(base_path):
        if '.git' in dirs:
            git_repos.append(root)
            dirs[:] = []  # Don't recurse into subdirectories of a repo
    return git_repos

def main():

    base_path = '/home/alex/pkg/'
    author_name = 'alexlenkoski'
    excluded_message = "Cleanup"
    target_date = get_target_date()
    
    total_changes = 0
    for repo_path in find_git_repos(base_path):
        total_changes += count_changes_in_repo(repo_path,
                                               target_date,
                                               'alexlenkoski',
                                               excluded_message)

    print(total_changes)

if __name__ == "__main__":
    main()

    #!/usr/bin/env python3

import os
import sys
import difflib
from datetime import datetime, date
from git import Repo

def get_target_date():
    if len(sys.argv) > 1:
        try:
            return datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    return date.today()

def is_git_repo(path):
    try:
        _ = Repo(path).git_dir
        return True
    except:
        return False

def process_commit(commit):

    words_changed = 0
    if not commit.parents:
        return 0, 0  # Skip root commit

    diffs = commit.diff(commit.parents[0], create_patch = True)
    for diff in diffs:
        if diff.a_path.endswith(('.tex', '.org')):
            patch = diff.diff.decode('utf-8', errors='ignore')
            lines = patch.splitlines()

            for line in lines:
                if line.startswith('+') and not line.startswith('+++'):
                    words_changed += len(line.split())
                if line.startswith('-') and not line.startswith('---'):
                    words_changed -= len(line.split())
    
    return words_changed

def main():
    base_path = "/home/alex/articles"
    author = "alexlenkoski"
    excluded_message = "Cleanup"
    target_date = get_target_date()

    grand_total_changed = 0

    for entry in os.listdir(base_path):
        repo_path = os.path.join(base_path, entry)
        if is_git_repo(repo_path):
            repo = Repo(repo_path)
            total_changed = 0
            for commit in repo.iter_commits():
                commit_date = datetime.fromtimestamp(commit.committed_date).date()
                right_date = (commit_date == target_date)
                right_author = (commit.author.name == author)
                not_exclude = (commit.message.strip() != excluded_message)
                process = all([right_date, right_author, not_exclude])
                if process:
                    changed = process_commit(commit)
                    total_changed += abs(changed)

                
            print(f"{entry}, Words Changed: {total_changed}")
            grand_total_changed += total_changed


    print(f"Grand total changed: {grand_total_changed}")

if __name__ == "__main__":
    main()

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
