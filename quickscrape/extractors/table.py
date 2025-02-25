from typing import List, Dict, Any, Optional
from .common import BaseExtractor
import pandas as pd

def extract_tables(html_content: str, **options) -> List[List[Dict[str, Any]]]:
    """
    Extract tables from HTML content.
    
    Args:
        html_content: HTML content to extract from.
        **options: Additional options for extraction.
            - include_headers: Whether to include table headers (default: True)
            - output_format: Format for output ('list', 'dict', 'dataframe') (default: 'list')
        
    Returns:
        List of extracted tables, each represented as a list of dictionaries.
    """
    soup = BaseExtractor.create_soup(html_content)
    
    # Find all tables in the HTML
    table_elements = soup.find_all('table')
    
    tables = []
    for table in table_elements:
        processed_table = process_table(table, **options)
        # if processed_table is data frame
        if isinstance(processed_table, pd.DataFrame):
            if not processed_table.empty:
                tables.append(processed_table)
        elif processed_table:  # Only add non-empty tables
            tables.append(processed_table)
    
    return tables


def process_table(table_element, **options) -> Optional[List[Dict[str, Any]]]:
    """
    Process a single table element into structured data.
    
    Args:
        table_element: BeautifulSoup table element.
        **options: Additional options for extraction.
            - include_headers: Whether to include table headers (default: True)
            - output_format: Format for output ('list', 'dict', 'dataframe') (default: 'list')
        
    Returns:
        Structured representation of the table, or None if table is invalid.
    """
    # Extract options with defaults
    include_headers = options.get('include_headers', True)
    output_format = options.get('output_format', 'list')
    
    # Get table headers
    headers = []
    header_row = table_element.find('thead')
    
    if header_row:
        th_elements = header_row.find_all('th')
        if th_elements:
            headers = [th.get_text(strip=True) for th in th_elements]
    
    # If no headers were found in thead, look in the first tr
    if not headers and include_headers:
        first_row = table_element.find('tr')
        if first_row:
            headers = [cell.get_text(strip=True) for cell in first_row.find_all(['th', 'td'])]
    
    # If still no headers or headers not needed, generate column names
    if not headers:
        # Find the row with the most cells to determine number of columns
        max_cells = 0
        for row in table_element.find_all('tr'):
            cells_count = len(row.find_all(['td', 'th']))
            max_cells = max(max_cells, cells_count)
        
        if max_cells > 0:
            headers = [f'Column {i+1}' for i in range(max_cells)]
        else:
            # No valid rows found
            return None
    
    # Process table rows
    rows = []
    data_rows = table_element.find('tbody')
    
    # If tbody exists, use its rows, otherwise use all tr elements
    if data_rows:
        tr_elements = data_rows.find_all('tr')
    else:
        tr_elements = table_element.find_all('tr')
        # Skip header row if we're using it as headers
        if include_headers and headers:
            tr_elements = tr_elements[1:]
    
    for row in tr_elements:
        cells = row.find_all(['td', 'th'])
        # Skip empty rows
        if not cells:
            continue
            
        # Extract text from each cell
        cell_data = [cell.get_text(strip=True) for cell in cells]
        
        # Handle case where row has fewer cells than headers
        if len(cell_data) < len(headers):
            cell_data.extend([''] * (len(headers) - len(cell_data)))
        
        # Handle case where row has more cells than headers
        elif len(cell_data) > len(headers):
            # Either truncate the extra cells or expand headers
            cell_data = cell_data[:len(headers)]
        
        # Create row data based on output format
        if output_format == 'dict':
            row_data = dict(zip(headers, cell_data))
        else:
            row_data = dict(zip(headers, cell_data))
        
        rows.append(row_data)
    
    # Discard the first row if it is the same as the headers
    if include_headers and rows and list(rows[0].values()) == headers:
        rows = rows[1:]
    
    # Convert to requested output format
    if output_format == 'dataframe':
        return pd.DataFrame(rows)
    else:
        return rows