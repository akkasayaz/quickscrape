from typing import Union, List, Dict, Any
from .utils.request import fetch_url
from .extractors import get_extractor


def extract(data_type: Union[str, List[str], Dict[str, str]], 
            url: str, 
            **options) -> Any:
    """
    Extract specified data type(s) from a URL.
    
    Args:
        data_type: Type of data to extract ("email", "table", etc.) or a list of types,
                  or a dictionary mapping names to CSS selectors.
        url: URL to scrape.
        **options: Additional options for extraction.
        
    Returns:
        Extracted data in the specified format.
    
    Examples:
        >>> import quickscrape
        >>> emails = quickscrape.extract("email", "https://example.com/contact")
        >>> tables = quickscrape.extract("table", "https://example.com/data")
    """
    # Fetch the page content
    html_content = fetch_url(url, **options)
    
    # Handle different types of data_type parameter
    if isinstance(data_type, str):
        # Single data type extraction
        extractor = get_extractor(data_type)
        return extractor(html_content, **options)
    
    elif isinstance(data_type, list):
        # Multiple data types extraction
        results = {}
        for dt in data_type:
            extractor = get_extractor(dt)
            results[dt] = extractor(html_content, **options)
        return results
    
    elif isinstance(data_type, dict):
        # Custom extraction with selectors
        # Implementation would use CSS selectors to extract content
        raise NotImplementedError("Custom extraction not yet implemented")
    
    else:
        raise ValueError(f"Unsupported data_type: {data_type}")