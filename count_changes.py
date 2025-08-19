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
