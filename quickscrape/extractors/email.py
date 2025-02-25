import re
from typing import List
from .common import BaseExtractor


def extract_emails(html_content: str, **options) -> List[str]:
    """
    Extract email addresses from HTML content.
    
    Args:
        html_content: HTML content to extract from.
        **options: Additional options for extraction.
        
        
    Returns:
        List of email addresses found.
    """
    # Create BeautifulSoup object
    soup = BaseExtractor.create_soup(html_content)
    
    # Convert to text to simplify email extraction
    text = soup.get_text(" ")
    
    # Regular expression for matching email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Find all email addresses
    emails = re.findall(email_pattern, text)
    
    # Remove duplicates while preserving order
    unique_emails = list(dict.fromkeys(emails))

    return unique_emails