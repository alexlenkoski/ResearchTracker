#!/usr/bin/env python3
import subprocess
from pathlib import Path

PAPERS_DIR = Path.home() / "articles"

def words_added_in_tex(repo_path):
    """Return number of words added in .tex files since 10am yesterday."""
    total_words = 0
    try:
        # Get diff of all .tex files since 10am yesterday
        output = subprocess.check_output(
            ["git", "diff", "--since=10am yesterday", "--", "*.tex"],
            cwd=repo_path,
            text=True
        )
    except subprocess.CalledProcessError:
        return 0

    for line in output.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            # Count words in added lines
            total_words += len(line[1:].split())
    return total_words

def main():
    total_words = 0
    for paper in PAPERS_DIR.iterdir():
        if (paper / ".git").is_dir():
            words = words_added_in_tex(paper)
            print(f"{paper.name}: {words} words added")
            total_words += words
    print(f"\nTotal words added across all papers: {total_words}")

if __name__ == "__main__":
    main()
