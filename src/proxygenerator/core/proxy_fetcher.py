#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Proxy fetcher module for retrieving proxy lists from external sources."""

import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class ProxyFetcher:
    """Handles fetching proxy lists from external sources."""
    
    def __init__(self, cache_dir='cache', data_dir='data'):
        self.cache_dir = cache_dir
        self.data_dir = data_dir
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure cache and data directories exist."""
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_proxy_list(self, url="https://free-proxy-list.net/#list"):
        """Fetch proxy list from the specified URL."""
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        cache_file = os.path.join(self.cache_dir, 'proxies.html')
        
        try:
            with urlopen(req, timeout=10) as response:
                html_content = response.read().decode('UTF-8')
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                return html_content
        except Exception as e:
            print(f'Error fetching proxy list: {e}')
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            raise
    
    def parse_proxy_list(self, html_content):
        """Parse HTML content to extract proxy information."""
        soup = BeautifulSoup(html_content, "lxml")
        table_body = soup.find('tbody')
        
        if not table_body:
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
        
        return proxies