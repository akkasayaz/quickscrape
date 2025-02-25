"""
Extractors for different data types.
"""

from .email import extract_emails
from .table import extract_tables

# Registry of available extractors
EXTRACTORS = {
    "email": extract_emails,
    "table": extract_tables,
    # Add more extractors as they are implemented
}


def get_extractor(data_type):
    """
    Get the appropriate extractor function for the specified data type.
    
    Args:
        data_type: Type of data to extract.
        
    Returns:
        Extractor function.
        
    Raises:
        ValueError: If no extractor exists for the specified data type.
    """
    if data_type not in EXTRACTORS:
        raise ValueError(f"No extractor available for data type: {data_type}")
    
    return EXTRACTORS[data_type]


__all__ = ["get_extractor", "EXTRACTORS"]