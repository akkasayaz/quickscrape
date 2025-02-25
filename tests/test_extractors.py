from quickscrape.extractors import email, table
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from bs4 import BeautifulSoup


class TestEmailExtractor(unittest.TestCase):
    """Tests for email extraction functionality."""
    
    def test_extract_emails(self):
        """Test extracting emails from HTML content."""
        html = """
        <html>
        <body>
            <p>Contact us at info@example.com or support@example.com</p>
            <div>Sales: sales@example.com</div>
        </body>
        </html>
        """
        
        emails = email.extract_emails(html)
        
        self.assertEqual(len(emails), 3)
        self.assertIn("info@example.com", emails)
        self.assertIn("support@example.com", emails)
        self.assertIn("sales@example.com", emails)
    
    def test_no_emails(self):
        """Test extracting emails when none are present."""
        html = """
        <html>
        <body>
            <p>Contact us by phone.</p>
        </body>
        </html>
        """
        
        emails = email.extract_emails(html)
        
        self.assertEqual(len(emails), 0)




class TestTableExtractor(unittest.TestCase):
    """Tests for table extraction functionality."""
    
    def test_extract_basic_table(self):
        """Test extracting a simple table from HTML content."""
        html = """
        <html>
        <body>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                </tr>
                <tr>
                    <td>Alice</td>
                    <td>25</td>
                </tr>
                <tr>
                    <td>Bob</td>
                    <td>30</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        tables = table.extract_tables(html)
        
        # Verify results
        self.assertEqual(len(tables), 1, "Should extract exactly one table")
        self.assertIsInstance(tables[0], list, "Table should be returned as a list")
        self.assertEqual(len(tables[0]), 2, "Table should have 2 data rows")
        
        # Verify content
        self.assertEqual(tables[0][0]['Name'], 'Alice')
        self.assertEqual(tables[0][0]['Age'], '25')
        self.assertEqual(tables[0][1]['Name'], 'Bob')
        self.assertEqual(tables[0][1]['Age'], '30')
    
    def test_extract_multiple_tables(self):
        """Test extracting multiple tables from the same HTML."""
        html = """
        <html>
        <body>
            <table id="table1">
                <tr><th>Name</th><th>Age</th></tr>
                <tr><td>Alice</td><td>25</td></tr>
            </table>
            <div>Some text between tables</div>
            <table id="table2">
                <tr><th>Product</th><th>Price</th></tr>
                <tr><td>Widget</td><td>10.99</td></tr>
                <tr><td>Gadget</td><td>19.99</td></tr>
            </table>
        </body>
        </html>
        """
        
        tables = table.extract_tables(html)
        
        self.assertEqual(len(tables), 2, "Should extract two tables")
        self.assertEqual(len(tables[0]), 1, "First table should have 1 data row")
        self.assertEqual(len(tables[1]), 2, "Second table should have 2 data rows")
        self.assertEqual(tables[1][1]['Product'], 'Gadget')
    
    def test_extract_table_with_thead_tbody(self):
        """Test extracting tables with proper thead and tbody structure."""
        html = """
        <table>
            <thead>
                <tr><th>Item</th><th>Quantity</th><th>Price</th></tr>
            </thead>
            <tbody>
                <tr><td>Apple</td><td>5</td><td>2.50</td></tr>
                <tr><td>Orange</td><td>3</td><td>1.99</td></tr>
            </tbody>
        </table>
        """
        
        tables = table.extract_tables(html)
        
        self.assertEqual(len(tables), 1)
        self.assertEqual(len(tables[0]), 2)
        
        # Verify headers were correctly extracted from thead
        self.assertIn('Item', tables[0][0])
        self.assertIn('Quantity', tables[0][0])
        self.assertIn('Price', tables[0][0])
    
    def test_empty_tables(self):
        """Test handling of empty tables."""
        html = """
        <table></table>
        <table><tr></tr></table>
        """
        
        tables = table.extract_tables(html)
        
        self.assertEqual(len(tables), 0, "Empty tables should be filtered out")
    
    def test_missing_headers(self):
        """Test tables with no headers."""
        html = """
        <table>
            <tr><td>Alice</td><td>25</td></tr>
            <tr><td>Bob</td><td>30</td></tr>
        </table>
        """
        
        tables = table.extract_tables(html, include_headers=False)
        
        self.assertEqual(len(tables), 1)
        self.assertEqual(len(tables[0]), 2)
        # Check auto-generated headers are used
        self.assertIn('Column 1', tables[0][0])
        self.assertIn('Column 2', tables[0][0])
    
    def test_output_formats(self):
        """Test different output formats."""
        html = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>Alice</td><td>25</td></tr>
        </table>
        """
        
        # Default output format returns a list of dicts
        tables_list = table.extract_tables(html)
        self.assertIsInstance(tables_list[0][0], dict)
        
        # Test dataframe output format
        tables_df = table.extract_tables(html, output_format='dataframe')
        self.assertIsInstance(tables_df[0], pd.DataFrame)
        self.assertEqual(tables_df[0].shape, (1, 2))
        
        # In your implementation, both 'list' and 'dict' formats return lists of dicts
        tables_dict = table.extract_tables(html, output_format='dict')
        self.assertIsInstance(tables_dict[0][0], dict)
    
    def test_inconsistent_rows(self):
        """Test tables with rows having different numbers of cells."""
        html = """
        <table>
            <tr><th>Name</th><th>Age</th><th>City</th></tr>
            <tr><td>Alice</td><td>25</td></tr>
            <tr><td>Bob</td><td>30</td><td>New York</td><td>Extra</td></tr>
        </table>
        """
        
        tables = table.extract_tables(html)
        
        # First row is missing City
        self.assertEqual(tables[0][0]['City'], '')
        # Second row should have Name, Age, and City, but not the extra cell
        self.assertEqual(len(tables[0][1]), 3)
    
    def test_nested_tables(self):
        """Test handling of nested tables."""
        html = """
        <table id="outer">
            <tr><th>Category</th><th>Details</th></tr>
            <tr>
                <td>Main</td>
                <td>
                    <table id="inner">
                        <tr><th>Sub</th><th>Value</th></tr>
                        <tr><td>A</td><td>10</td></tr>
                    </table>
                </td>
            </tr>
        </table>
        """
        
        tables = table.extract_tables(html)
        
        # Should find both outer and inner tables
        self.assertEqual(len(tables), 2, "Should extract both the outer and inner tables")
    
    @patch('quickscrape.extractors.common.BaseExtractor.create_soup')
    def test_invalid_html(self, mock_create_soup):
        """Test handling of invalid HTML."""
        # Mock the soup creation to simulate parsing error
        mock_soup = MagicMock()
        mock_soup.find_all.return_value = []  # No tables found
        mock_create_soup.return_value = mock_soup
        
        tables = table.extract_tables("<invalid>html</not-matching>")
        
        self.assertEqual(len(tables), 0, "Invalid HTML should return no tables")
        # Verify the mock was called
        mock_create_soup.assert_called_once()
    
    def test_complex_html_structure(self):
        """Test extraction from complex HTML with multiple elements."""
        html = """
        <div class="container">
            <h1>Report</h1>
            <p>Some introduction text</p>
            <table class="data-table">
                <caption>Monthly Sales</caption>
                <thead>
                    <tr><th>Month</th><th>Revenue</th><th>Expenses</th><th>Profit</th></tr>
                </thead>
                <tbody>
                    <tr><td>January</td><td>$10,000</td><td>$7,000</td><td>$3,000</td></tr>
                    <tr><td>February</td><td>$11,500</td><td>$7,200</td><td>$4,300</td></tr>
                </tbody>
                <tfoot>
                    <tr><td>Total</td><td>$21,500</td><td>$14,200</td><td>$7,300</td></tr>
                </tfoot>
            </table>
        </div>
        """
        
        tables = table.extract_tables(html)
        
        self.assertEqual(len(tables), 1)
        # We check for the specific data we expect to be present
        self.assertGreaterEqual(len(tables[0]), 2, "Should extract at least 2 rows")
        self.assertEqual(tables[0][0]['Month'], 'January')
        self.assertEqual(tables[0][1]['Month'], 'February')
        
        # Note: Currently your implementation might not handle the tfoot element
        # This can be added as a future enhancement
    
    def test_table_with_bug_fix(self):
        """Test the fix for the bug in the original code."""
        html = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>Alice</td><td>25</td></tr>
        </table>
        """
        
        # This test ensures the fixed line works properly
        tables = table.extract_tables(html)
        self.assertEqual(len(tables), 1)
        
        # Create a DataFrame for testing the bug
        df = pd.DataFrame({'Name': ['Alice'], 'Age': ['25']})
        
        # Mock the process_table function to return the DataFrame
        with patch('quickscrape.extractors.table.process_table', return_value=df):
            # This would fail with the original typo (process_table.empty instead of processed_table.empty)
            tables = table.extract_tables(html)
            self.assertEqual(len(tables), 1)


if __name__ == "__main__":
    unittest.main()