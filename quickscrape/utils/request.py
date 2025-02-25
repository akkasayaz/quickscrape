"""
HTTP request handling for QuickScrape.
"""

import requests
from typing import Dict, Any, Optional


def fetch_url(url: str, 
              timeout: int = 10, 
              headers: Optional[Dict[str, str]] = None,
              **options) -> str:
    """
    Fetch HTML content from a URL.
    
    Args:
        url: URL to fetch.
        timeout: Request timeout in seconds.
        headers: Custom headers for the request.
        **options: Additional options for the request.
        
    Returns:
        HTML content as string.
        
    Raises:
        ValueError: If the URL is invalid or not accessible.
    """
    # Default headers with User-Agent
    default_headers = {
        'User-Agent': 'QuickScrape/0.1.0'
    }
    
    # Combine default headers with custom headers
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.get(url, headers=default_headers, timeout=timeout)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # Ensure we're dealing with HTML content
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type and not options.get('force', False):
            raise ValueError(f"URL does not contain HTML content: {content_type}")
        
        return response.text
    
    except requests.RequestException as e:
        raise ValueError(f"Error fetching URL: {str(e)}")