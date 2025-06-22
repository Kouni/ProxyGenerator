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
data = requests.get('https://kouni.github.io/ProxyGenerator/proxies.json').json()
metadata = data['metadata']  # Generated time, count, source info
proxies = data['proxies']    # List of proxy objects
```

## Implementation

- Source: free-proxy-list.net
- Validation: 5s timeout with IP verification
- Refresh: GitHub Actions hourly
- Format: JSON with metadata

## Requirements

Python 3.13+ | Poetry | beautifulsoup4 | lxml