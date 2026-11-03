import sys
import os
import json
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from indexer import tokenize, build_index, save_index, load_index


class TestTokenize:
    def test_lowercase(self):
        assert tokenize("Hello World") == ["hello", "world"]

    def test_removes_punctuation(self):
        assert tokenize("hello, world!") == ["hello", "world"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_numbers_excluded(self):
        assert tokenize("abc 123 def") == ["abc", "def"]

    def test_mixed_case(self):
        assert tokenize("Good GOOD good") == ["good", "good", "good"]


class TestBuildIndex:
    def test_single_page(self):
        pages = {"http://example.com": "hello world hello"}
        index = build_index(pages)
        assert "hello" in index
        assert index["hello"]["http://example.com"]["frequency"] == 2

    def test_multiple_pages(self):
        pages = {
            "http://example.com/1": "hello world",
            "http://example.com/2": "hello python"
        }
        index = build_index(pages)
        assert len(index["hello"]) == 2

    def test_positions_recorded(self):
        pages = {"http://example.com": "a b a"}
        index = build_index(pages)
        assert index["a"]["http://example.com"]["positions"] == [0, 2]

    def test_empty_pages(self):
        index = build_index({})
        assert index == {}

    def test_case_insensitive(self):
        pages = {"http://example.com": "Good good GOOD"}
        index = build_index(pages)
        assert index["good"]["http://example.com"]["frequency"] == 3


class TestSaveLoadIndex:
    def test_save_and_load(self):
        index = {"hello": {"http://example.com": {"frequency": 1, "positions": [0]}}}
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
            tmpfile = f.name
        save_index(index, tmpfile)
        loaded = load_index(tmpfile)
        assert loaded == index
        os.unlink(tmpfile)

    def test_load_missing_file(self):
        result = load_index("nonexistent_file.json")
        assert result is None
