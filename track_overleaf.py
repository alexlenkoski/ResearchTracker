import os
import json
from datetime import datetime
from pathlib import Path
# Config
ROOT_DIR = Path.home() / 'articles'
TRACKER_DIR = Path.home() / 'pkg/TheInquiry/ResearchTracker'
DATA_FILE = TRACKER_DIR / "word_count_history.json"
TEX_EXTENSIONS = [".tex"]

def count_words_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    # Split on whitespace to count words
    return len(text.split())

def count_words_in_dir(root_dir=ROOT_DIR):
    total_words = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if any(fname.endswith(ext) for ext in TEX_EXTENSIONS):
                full_path = os.path.join(dirpath, fname)
                total_words += count_words_in_file(full_path)
    return total_words

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def main():
    history = load_history()
    today = datetime.now().strftime('%Y-%m-%d-%H-%M')
    current_count = count_words_in_dir()
    
    # Get previous count (most recent)
    if history:
        last_date, last_count = sorted(history.items())[-1]
        delta = current_count - last_count
        print(f"Word count today ({today}): {current_count}")
        print(f"Previous count ({last_date}): {last_count}")
        print(f"Change: {delta:+} words")
    else:
        print(f"Word count today ({today}): {current_count}")
        print("No previous data to compare.")

    # Save current count
    history[today] = current_count
    save_history(history)

if __name__ == "__main__":
    main()
