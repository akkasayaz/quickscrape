from typing import Any, Callable, Optional
from bs4 import BeautifulSoup


class BaseExtractor:
    """Base class for extractors with common functionality."""
    
    @staticmethod
    def create_soup(html_content: str) -> BeautifulSoup:
        """
        Create a BeautifulSoup object from HTML content.
        
        Args:
            html_content: HTML content to parse.
            
        Returns:
            BeautifulSoup object.
        """
        return BeautifulSoup(html_content, "html.parser")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted text by removing extra whitespace, etc.
        
        Args:
            text: Text to clean.
            
        Returns:
            Cleaned text.
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        return " ".join(text.split())


def extract_with_selector(html_content: str, 
                          selector: str, 
                          attribute: Optional[str] = None,
                          transform: Optional[Callable] = None) -> Any:
    """
    Extract data from HTML using a CSS selector.
    
    Args:
        html_content: HTML content to extract from.
        selector: CSS selector to use.
        attribute: HTML attribute to extract (if None, extracts text).
        transform: Function to transform the extracted data.
        
    Returns:
        Extracted data.
    """
    soup = BaseExtractor.create_soup(html_content)
    elements = soup.select(selector)
    
    results = []
    for element in elements:
        if attribute:
            value = element.get(attribute, "")
        else:
            value = element.text
            value = BaseExtractor.clean_text(value)
            
        if transform and value:
            value = transform(value)
            
        results.append(value)
    
    return results