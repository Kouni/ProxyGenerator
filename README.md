# ProxyGenerator

HTTP proxy fetcher with automated validation and hourly refresh.

## Usage

```bash
poetry install
poetry run proxygenerator
```

Fresh proxy data: [Download JSON](https://kouni.github.io/ProxyGenerator/proxies.json)

## Data Access

```bash
# Direct download
curl -O https://kouni.github.io/ProxyGenerator/proxies.json

# Use in Python
import requests
proxies = requests.get('https://kouni.github.io/ProxyGenerator/proxies.json').json()
# Format: [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080', ...}]
```

## Implementation

- Source: free-proxy-list.net
- Validation: 5s timeout with IP verification
- Refresh: GitHub Actions hourly
- Format: JSON with metadata

## Requirements

Python 3.13+ | Poetry | beautifulsoup4 | lxml