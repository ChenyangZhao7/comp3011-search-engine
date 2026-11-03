import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search import print_word, find_pages


# Sample index for testing
SAMPLE_INDEX = {
    "hello": {
        "http://example.com/1": {"frequency": 2, "positions": [0, 5]},
        "http://example.com/2": {"frequency": 1, "positions": [3]}
    },
    "world": {
        "http://example.com/1": {"frequency": 1, "positions": [1]},
        "http://example.com/3": {"frequency": 2, "positions": [0, 4]}
    },
    "python": {
        "http://example.com/2": {"frequency": 1, "positions": [0]}
    }
}


class TestPrintWord:
    def test_existing_word(self, capsys):
        print_word(SAMPLE_INDEX, "hello")
        captured = capsys.readouterr()
        assert "hello" in captured.out
        assert "http://example.com/1" in captured.out

    def test_missing_word(self, capsys):
        print_word(SAMPLE_INDEX, "missing")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_case_insensitive(self, capsys):
        print_word(SAMPLE_INDEX, "HELLO")
        captured = capsys.readouterr()
        assert "hello" in captured.out

    def test_empty_word(self, capsys):
        print_word(SAMPLE_INDEX, "")
        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestFindPages:
    def test_single_word(self, capsys):
        find_pages(SAMPLE_INDEX, "hello")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out
        assert "http://example.com/2" in captured.out

    def test_multi_word(self, capsys):
        find_pages(SAMPLE_INDEX, "hello world")
        captured = capsys.readouterr()
        # Only page 1 contains both hello and world
        assert "http://example.com/1" in captured.out
        assert "http://example.com/2" not in captured.out

    def test_missing_word(self, capsys):
        find_pages(SAMPLE_INDEX, "missing")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_empty_query(self, capsys):
        find_pages(SAMPLE_INDEX, "")
        captured = capsys.readouterr()
        assert "empty" in captured.out

    def test_no_common_pages(self, capsys):
        find_pages(SAMPLE_INDEX, "python world")
        captured = capsys.readouterr()
        assert "No pages found" in captured.out

    def test_case_insensitive(self, capsys):
        find_pages(SAMPLE_INDEX, "HELLO")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out
