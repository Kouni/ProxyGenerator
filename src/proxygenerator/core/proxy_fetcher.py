#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Proxy fetcher module for retrieving proxy lists from external sources."""

import logging
import os
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ProxyFetcher:
    """Handles fetching proxy lists from external sources."""

    # Security: Whitelist of trusted proxy sources
    TRUSTED_HOSTS = {
        'free-proxy-list.net',
        'www.free-proxy-list.net'
    }

    def __init__(self, cache_dir='cache', data_dir='data'):
        self.cache_dir = cache_dir
        self.data_dir = data_dir
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure cache and data directories exist."""
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

    def _validate_url(self, url):
        """Validate URL against trusted hosts to prevent SSRF attacks."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.hostname:
                raise ValueError("Invalid URL format")

            if parsed.scheme not in ('http', 'https'):
                raise ValueError("Only HTTP/HTTPS URLs are allowed")

            if parsed.hostname not in self.TRUSTED_HOSTS:
                raise ValueError(f"Untrusted host: {parsed.hostname}")

            return True
        except (AttributeError, TypeError) as e:
            logger.error("URL parsing error for %s: %s", url, e)
            raise ValueError(f"Invalid URL format: {url}") from e

    def fetch_proxy_list(self, url="https://free-proxy-list.net/#list"):
        """Fetch proxy list from the specified URL."""
        # Security: Validate URL before making request
        self._validate_url(url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        cache_file = os.path.join(self.cache_dir, 'proxies.html')

        try:
            with urlopen(req, timeout=10) as response:
                html_content = response.read().decode('UTF-8')
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info("Successfully fetched proxy list from %s", url)
                return html_content
        except (ConnectionError, TimeoutError, URLError) as e:
            logger.warning("Network error fetching proxy list: %s", e)
            if os.path.exists(cache_file):
                logger.info("Using cached proxy list due to network error")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            raise
        except UnicodeDecodeError as e:
            logger.error("Failed to decode response content: %s", e)
            raise
        except OSError as e:
            logger.error("File I/O error: %s", e)
            raise

    def parse_proxy_list(self, html_content):
        """Parse HTML content to extract proxy information."""
        try:
            soup = BeautifulSoup(html_content, "lxml")
            table_body = soup.find('tbody')

            if not table_body:
                logger.warning("No table body found in HTML content")
                return []

            proxies = []
            for row in table_body.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 8:
                    proxy_info = {
                        'IP_Address_td': cells[0].string,
                        'Port_td': cells[1].string,
                        'Code_td': cells[2].string,
                        'Country_td': cells[3].string,
                        'Anonymity_td': cells[4].string,
                        'Google_td': cells[5].string,
                        'Https_td': cells[6].string,
                        'Last_Checked_td': cells[7].string
                    }
                    proxies.append(proxy_info)

            logger.info("Successfully parsed %d proxies from HTML", len(proxies))
            return proxies
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error parsing HTML content: %s", e)
            return []
