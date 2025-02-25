# QuickScrape

A simple Python library for extracting common data types from web pages.

## Installation

```bash
pip install quickscrape
```

## Usage

```python-repl
import quickscrape

# Extract emails from a webpage
emails = quickscrape.extract("email", "https://example.com/contact")

# Extract tables
tables = quickscrape.extract("table", "https://example.com/data")
```


## License

MIT



### Development Workflow

1. **Local Development**: Install your package in development mode:

   ```bash
   pip install -e .
   ```
2. **Testing** : Use pytest for writing and running tests.

   ```bash
   pip install pytest
   pytest
   ```
