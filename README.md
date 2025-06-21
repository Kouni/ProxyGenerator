# ProxyGenerator

HTTP proxy fetcher with automated validation and hourly refresh.

## Usage

```bash
poetry install
poetry run proxygenerator
```

Fresh proxy data: [`data/proxies.json`](data/proxies.json)

## Data Access

Direct JSON consumption:
```python
import json
with open('data/proxies.json') as f:
    proxies = json.load(f)
# Format: [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080', ...}]
```

## Implementation

- Source: free-proxy-list.net
- Validation: 5s timeout with IP verification
- Refresh: GitHub Actions hourly
- Format: JSON with metadata

## Requirements

Python 3.13+ | Poetry | beautifulsoup4 | lxml