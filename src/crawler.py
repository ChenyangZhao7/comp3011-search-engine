import requests
from bs4 import BeautifulSoup
import time
from typing import Optional, Tuple, Set, Dict, List

BASE_URL: str = "https://quotes.toscrape.com"
POLITENESS_WINDOW: int = 6


def get_page(url: str) -> Optional[str]:
    """
    Fetch a single page and return its HTML content.

    Args:
        url: The URL of the page to fetch.

    Returns:
        The HTML content as a string, or None if the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_page(html: str, url: str) -> Tuple[str, Set[str]]:
    """
    Parse HTML and extract text content and internal links.

    Args:
        html: Raw HTML content of the page.
        url: The URL of the page.

    Returns:
        A tuple of (text content, set of internal links found).
    """
    soup = BeautifulSoup(html, "html.parser")
    text: str = soup.get_text(separator=" ", strip=True)

    links: Set[str] = set()
    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"]
        if href.startswith("/"):
            links.add(BASE_URL + href)

    return text, links


def crawl(start_url: str = BASE_URL) -> Dict[str, str]:
    """
    Crawl the website starting from start_url using BFS.

    Respects a politeness window of 6 seconds between requests.

    Args:
        start_url: The URL to begin crawling from.

    Returns:
        A dictionary mapping each visited URL to its text content.
    """
    visited: Set[str] = set()
    to_visit: List[str] = [start_url]
    pages: Dict[str, str] = {}

    while to_visit:
        url: str = to_visit.pop(0)

        if url in visited:
            continue

        print(f"Crawling: {url}")
        html = get_page(url)

        if html is None:
            continue

        visited.add(url)
        text, links = parse_page(html, url)
        pages[url] = text

        for link in links:
            if link not in visited:
                to_visit.append(link)

        if to_visit:
            time.sleep(POLITENESS_WINDOW)

    print(f"Crawling complete. {len(pages)} pages visited.")
    return pages
