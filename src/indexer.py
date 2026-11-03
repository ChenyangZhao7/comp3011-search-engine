import json
import re

INDEX_FILE = "data/index.json"


def tokenize(text):
    """Convert text to lowercase tokens, removing punctuation."""
    text = text.lower()
    tokens = re.findall(r'[a-z]+', text)
    return tokens


def build_index(pages):
    """Build an inverted index from crawled pages.
    
    Structure:
    {
        "word": {
            "url1": {"frequency": 3, "positions": [1, 5, 12]},
            "url2": {"frequency": 1, "positions": [7]}
        }
    }
    """
    index = {}

    for url, text in pages.items():
        tokens = tokenize(text)

        for position, word in enumerate(tokens):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {"frequency": 0, "positions": []}

            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)

    return index


def save_index(index, filepath=INDEX_FILE):
    """Save index to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print(f"Index saved to {filepath}")


def load_index(filepath=INDEX_FILE):
    """Load index from a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            index = json.load(f)
        print(f"Index loaded from {filepath}")
        return index
    except FileNotFoundError:
        print(f"Error: No index file found at {filepath}. Run 'build' first.")
        return None
