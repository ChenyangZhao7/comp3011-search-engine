import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search import print_word, find_pages, find_phrase


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

    def test_punctuation_ignored(self, capsys):
        find_pages(SAMPLE_INDEX, "hello, world!")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out


# Index where "good friends" is adjacent on page 1 but not on page 2
PHRASE_INDEX = {
    "good": {
        "http://example.com/1": {"frequency": 1, "positions": [0]},
        "http://example.com/2": {"frequency": 1, "positions": [0]}
    },
    "friends": {
        "http://example.com/1": {"frequency": 1, "positions": [1]},
        "http://example.com/2": {"frequency": 1, "positions": [5]}
    },
    "life": {
        "http://example.com/1": {"frequency": 1, "positions": [2]}
    }
}


class TestFindPhrase:
    def test_phrase_present(self, capsys):
        find_phrase(PHRASE_INDEX, "good friends")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out
        assert "http://example.com/2" not in captured.out

    def test_words_present_but_not_adjacent(self, capsys):
        find_phrase(PHRASE_INDEX, "friends good")
        captured = capsys.readouterr()
        assert "No pages found" in captured.out

    def test_three_word_phrase(self, capsys):
        find_phrase(PHRASE_INDEX, "good friends life")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out
        assert "phrase frequency: 1" in captured.out

    def test_case_and_punctuation_insensitive(self, capsys):
        find_phrase(PHRASE_INDEX, "GOOD, friends!")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out

    def test_single_word(self, capsys):
        find_phrase(PHRASE_INDEX, "life")
        captured = capsys.readouterr()
        assert "http://example.com/1" in captured.out
        assert "phrase frequency: 1" in captured.out

    def test_missing_word(self, capsys):
        find_phrase(PHRASE_INDEX, "good missing")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_empty_query(self, capsys):
        find_phrase(PHRASE_INDEX, "")
        captured = capsys.readouterr()
        assert "empty" in captured.out
