# ProxyGenerator

Secure HTTP proxy fetcher with automated validation, concurrent processing, and hourly refresh.

## Features

- **Security-First**: HTTP validation with comprehensive input validation and SSRF protection
- **Input Validation**: IP address and port range validation with private/loopback filtering
- **Concurrent Processing**: Multi-threaded proxy validation for improved performance
- **Automated Refresh**: GitHub Actions scheduled execution every hour
- **Production Quality**: 100% test coverage (34/34 tests) with 10/10 Pylint score

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

## Security Features

- **SSRF Protection**: Trusted host whitelist prevents server-side request forgery
- **Protocol Validation**: HTTP testing optimized for proxy compatibility
- **Input Sanitization**: IP address format validation and private network filtering
- **Dependency Scanning**: Automated security vulnerability checks in CI/CD

## Architecture

- **Modular Design**: Separated concerns for fetching, validation, and file handling
- **Concurrent Validation**: ThreadPoolExecutor for parallel proxy testing
- **Error Handling**: Specific exception types with comprehensive logging
- **Caching Strategy**: Local cache with fallback for network failures
- **Code Quality**: 10/10 Pylint score with production-ready standards

## Implementation Details

- **Source**: free-proxy-list.net (whitelisted for security)
- **Validation**: 5s timeout with HTTP IP verification for broad compatibility
- **Refresh**: GitHub Actions hourly with security scanning
- **Format**: JSON with metadata and generation timestamps
- **Performance**: Concurrent validation with configurable worker threads

## Development

```bash
# Install dependencies
poetry install

# Run tests with coverage (34/34 tests, 100% coverage)
poetry run pytest --cov=src tests/

# Security scan (requires SAFETY_API_KEY environment variable)
export SAFETY_API_KEY=your_api_key
poetry run safety scan

# Note: In CI/CD, the workflow automatically handles interactive prompts

# Code quality check (achieves 10/10 score)
poetry run pylint src/

# Format checking
poetry run isort --check-only src/ tests/
```

## Quality Metrics

- **Test Coverage**: 100% (34/34 tests passing)
- **Code Quality**: 10.00/10 Pylint score (production standard)
- **Security**: Zero known vulnerabilities with automated scanning
- **Performance**: Concurrent proxy validation with configurable workers

## Requirements

- **Runtime**: Python 3.13+, Poetry package manager
- **Core Dependencies**: beautifulsoup4, lxml
- **Development**: safety, pylint, pytest, pytest-cov, isort
- **CI/CD**: GitHub Actions with automated testing and security scanning