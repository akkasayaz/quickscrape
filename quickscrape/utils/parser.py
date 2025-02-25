from bs4 import BeautifulSoup
from typing import Optional


def parse_html(html_content: str, parser: str = "html.parser") -> BeautifulSoup:
    """
    Parse HTML content into a BeautifulSoup object.
    
    Args:
        html_content: HTML content to parse.
        parser: BeautifulSoup parser to use.
        
    Returns:
        BeautifulSoup object.
    """
    return BeautifulSoup(html_content, parser)


def extract_text_from_selector(soup: BeautifulSoup, 
                              selector: str,
                              clean: bool = True) -> Optional[str]:
    """
    Extract text from an element matching a CSS selector.
    
    Args:
        soup: BeautifulSoup object.
        selector: CSS selector to match.
        clean: Whether to clean the extracted text.
        
    Returns:
        Extracted text, or None if no match.
    """
    element = soup.select_one(selector)
    if not element:
        return None
    
    text = element.get_text()
    
    if clean:
        text = " ".join(text.split())
    
    return text