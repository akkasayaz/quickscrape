from urllib.parse import urlparse, urljoin
from typing import List, Optional
from .common import BaseExtractor


def extract_links(html_content: str, base_url: str, link_type: Optional[str] = None) -> List[str]:
    """
    Extract all links (URLs) from an HTML page with filtering options for internal/external links.

    Args:
        html_content: The HTML content to parse.
        base_url: The base URL of the page to determine internal/external links.
        link_type: Type of links to extract ('internal', 'external', or None for all).

    Returns:
        A list of extracted URLs.
    """
    soup = BaseExtractor.create_soup(html_content)

    # Parse the base URL to get its domain
    base_domain = urlparse(base_url).netloc

    internal_links = set()
    external_links = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.startswith("#"):
            continue
        # Convert relative URLs to absolute
        absolute_url = urljoin(base_url, href)
        parsed_url = urlparse(absolute_url)

        isInternal = parsed_url.netloc == base_domain

        (internal_links if isInternal else external_links).add(absolute_url)



    return list(internal_links) if link_type == "internal" else list(external_links) if link_type == "external" else list(internal_links.union(external_links))
