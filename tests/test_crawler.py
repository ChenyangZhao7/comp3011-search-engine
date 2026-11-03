import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawler import get_page, parse_page, BASE_URL


class TestGetPage:
    def test_successful_request(self):
        mock_response = MagicMock()
        mock_response.text = "<html><body>Hello</body></html>"
        mock_response.raise_for_status = MagicMock()

        with patch("crawler.requests.get", return_value=mock_response):
            result = get_page("http://example.com")
            assert result == "<html><body>Hello</body></html>"

    def test_failed_request(self):
        import requests
        with patch("crawler.requests.get", side_effect=requests.RequestException("error")):
            result = get_page("http://example.com")
            assert result is None

    def test_returns_none_on_error(self):
        with patch("crawler.requests.get", side_effect=Exception("error")):
            result = get_page("http://example.com")
            assert result is None


class TestParsePage:
    def test_extracts_text(self):
        html = "<html><body><p>Hello World</p></body></html>"
        text, links = parse_page(html, "http://example.com")
        assert "Hello" in text
        assert "World" in text

    def test_extracts_internal_links(self):
        html = '<html><body><a href="/page/1/">link</a></body></html>'
        text, links = parse_page(html, "http://example.com")
        assert BASE_URL + "/page/1/" in links

    def test_ignores_external_links(self):
        html = '<html><body><a href="http://external.com">link</a></body></html>'
        text, links = parse_page(html, "http://example.com")
        assert "http://external.com" not in links

    def test_empty_page(self):
        html = "<html><body></body></html>"
        text, links = parse_page(html, "http://example.com")
        assert links == set()

    def test_no_duplicate_links(self):
        html = '''<html><body>
            <a href="/page/1/">link</a>
            <a href="/page/1/">link again</a>
        </body></html>'''
        text, links = parse_page(html, "http://example.com")
        assert len([l for l in links if l == BASE_URL + "/page/1/"]) == 1
