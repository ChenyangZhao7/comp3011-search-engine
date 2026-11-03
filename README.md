# COMP3011 Search Engine Tool

A command-line search engine that crawls [quotes.toscrape.com](https://quotes.toscrape.com), builds an inverted index, and allows users to search for words and phrases across all crawled pages.

## Project Structure

    comp3011-search-engine/
    ├── src/
    │   ├── crawler.py      # Web crawler with politeness window
    │   ├── indexer.py      # Inverted index builder and storage
    │   ├── search.py       # Search and print logic
    │   └── main.py         # Command-line interface (cmd.Cmd)
    ├── tests/
    │   ├── test_crawler.py
    │   ├── test_indexer.py
    │   └── test_search.py
    ├── data/
    │   └── index.json      # Compiled inverted index
    ├── requirements.txt
    └── README.md

## Installation

    pip install -r requirements.txt

## Usage

Start the interactive shell:

    python3 src/main.py

### Commands

| Command | Description | Example |
|--------|-------------|---------|
| `build` | Crawl the website and build the index | `> build` |
| `load` | Load a previously built index from disk | `> load` |
| `print <word>` | Print the inverted index entry for a word | `> print life` |
| `find <query>` | Find all pages containing the query words | `> find good friends` |
| `help` | List all available commands | `> help` |
| `quit` | Exit the tool | `> quit` |

## Testing

    python3 -m pytest tests/ -v

## Dependencies

- `requests` — HTTP requests for web crawling
- `beautifulsoup4` — HTML parsing
- `pytest` — Testing framework

## Design Decisions

- **Inverted index stored as JSON** — human-readable, easy to inspect and debug
- **BFS crawling** — ensures all pages are visited level by level
- **6-second politeness window** — respects the target server
- **cmd.Cmd shell** — provides built-in help, command dispatching, and clean structure
- **Case-insensitive indexing** — all tokens lowercased at index build time
