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

                
            print(f"Repository: {entry}, Words Changed: {total_changed}")
            grand_total_changed += total_changed


        print(f"Grand total changed: {grand_total_changed}")

if __name__ == "__main__":
    main()
