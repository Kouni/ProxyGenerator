# ProxyGenerator

A Python application that fetches and validates proxy servers from free-proxy-list.net. This tool automatically retrieves proxy lists, validates their functionality, and provides working proxy servers for your applications.

## Features

- **Automatic Proxy Fetching**: Retrieves fresh proxy lists from free-proxy-list.net
- **Proxy Validation**: Tests each proxy to ensure functionality
- **Smart Caching**: Refreshes data only when needed (every 5 minutes)
- **Invalid Proxy Cleanup**: Automatically removes non-working proxies
- **Modular Architecture**: Clean, maintainable code structure
- **Poetry Integration**: Modern Python package management

## Requirements

- Python 3.13+
- Poetry

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ProxyGenerator
```

2. Install dependencies:
```bash
poetry install
```

## Usage

### Command Line
```bash
poetry run proxygenerator
```

### Programmatic Usage
```python
from proxygenerator.core.proxy_manager import ProxyManager

manager = ProxyManager()

# Get a working proxy
result = manager.find_working_proxy()
if result:
    print(f"Working proxy: {result['proxy']}")
    print(f"External IP: {result['result_ip']}")

# Get proxy statistics
stats = manager.get_stats()
print(f"Total proxies: {stats['count']}")
```

## Project Structure

```
ProxyGenerator/
├── src/proxygenerator/
│   ├── core/                   # Core functionality
│   │   ├── proxy_fetcher.py   # Proxy list fetching and parsing
│   │   ├── proxy_validator.py # Proxy validation and testing
│   │   └── proxy_manager.py   # Main management logic
│   ├── utils/                 # Utility functions
│   │   └── file_handler.py    # File operations and data persistence
│   └── main.py               # Application entry point
├── tests/                     # Test files
├── cache/                     # HTML cache files
├── data/                      # JSON data files
├── pyproject.toml            # Poetry configuration
└── README.md                 # This file
```

## How It Works

1. **Data Freshness Check**: Verifies if cached proxy data is newer than 5 minutes
2. **Proxy Fetching**: Downloads HTML from free-proxy-list.net if refresh needed
3. **HTML Parsing**: Extracts proxy information using BeautifulSoup
4. **Proxy Testing**: Validates each proxy by testing external IP retrieval
5. **Data Cleanup**: Removes invalid proxies and updates the cache
6. **Result Output**: Returns a working proxy with connection details

## Configuration

The application uses the following default settings:
- **Data refresh interval**: 300 seconds (5 minutes)
- **Proxy validation timeout**: 5 seconds
- **Test URL**: http://ifconfig.co/ip
- **Cache directory**: `cache/`
- **Data directory**: `data/`

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run isort .
poetry run pylint src/
```

## License

MIT License - see LICENSE file for details.
