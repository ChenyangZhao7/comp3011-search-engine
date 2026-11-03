import sys
import os
import cmd

sys.path.insert(0, os.path.dirname(__file__))

from crawler import crawl
from indexer import build_index, save_index, load_index
from search import print_word, find_pages


class SearchShell(cmd.Cmd):
    """Interactive shell for the search engine tool."""

    intro = (
        "\nSearch Engine Tool - COMP3011\n"
        "Type 'help' for a list of commands.\n"
        + "-" * 50
    )
    prompt = "\n> "

    def __init__(self):
        super().__init__()
        self.index = None

    def do_build(self, _):
        """Build the inverted index by crawling the website.\nUsage: build"""
        print("Starting crawl... (this will take a few minutes)")
        pages = crawl()
        self.index = build_index(pages)
        save_index(self.index)
        print(f"Done. Index contains {len(self.index)} unique words.")

    def do_load(self, _):
        """Load the index from the file system.\nUsage: load"""
        self.index = load_index()
        if self.index:
            print(f"Index loaded with {len(self.index)} unique words.")

    def do_print(self, word):
        """Print the inverted index entry for a word.\nUsage: print <word>"""
        if not word.strip():
            print("Usage: print <word>")
            return
        if self.index is None:
            print("No index loaded. Run 'build' or 'load' first.")
            return
        print_word(self.index, word.strip())

    def do_find(self, query):
        """Find pages containing all words in the query.\nUsage: find <word> [word2] ..."""
        if not query.strip():
            print("Usage: find <word> [word2] ...")
            return
        if self.index is None:
            print("No index loaded. Run 'build' or 'load' first.")
            return
        find_pages(self.index, query.strip())

    def do_quit(self, _):
        """Exit the search tool.\nUsage: quit"""
        print("Goodbye!")
        return True

    def do_EOF(self, _):
        """Handle Ctrl+D to exit."""
        print("\nGoodbye!")
        return True

    def emptyline(self):
        """Do nothing on empty input."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: '{line.split()[0]}'. Type 'help' for available commands.")


def main():
    SearchShell().cmdloop()


if __name__ == "__main__":
    main()
