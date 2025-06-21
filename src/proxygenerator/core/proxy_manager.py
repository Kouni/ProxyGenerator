#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Main proxy management module."""

import logging
import random
from .proxy_fetcher import ProxyFetcher
from .proxy_validator import ProxyValidator
from ..utils.file_handler import FileHandler

logger = logging.getLogger(__name__)


class ProxyManager:
    """Main proxy management class that coordinates all operations."""
    
    def __init__(self, cache_dir='cache', data_dir='data'):
        self.fetcher = ProxyFetcher(cache_dir, data_dir)
        self.validator = ProxyValidator()
        self.file_handler = FileHandler(data_dir)
    
    def refresh_proxy_data(self):
        """Fetch and save fresh proxy data."""
        try:
            logger.info("Starting proxy data refresh")
            html_content = self.fetcher.fetch_proxy_list()
            proxy_list = self.fetcher.parse_proxy_list(html_content)
            
            if proxy_list:
                self.file_handler.save_proxies(proxy_list)
                logger.info(f"Successfully refreshed proxy data with {len(proxy_list)} proxies")
                return True
            else:
                logger.warning("No proxies found during refresh")
                return False
        except Exception as e:
            logger.error(f'Unexpected error refreshing proxy data: {e}')
            return False
    
    def get_proxy_list(self, force_refresh=False):
        """Get proxy list, refreshing if necessary."""
        if force_refresh or not self.file_handler.is_data_fresh():
            logger.info("Proxy data is stale or refresh forced, attempting refresh")
            if not self.refresh_proxy_data():
                logger.warning('Failed to refresh proxy data, using cached data if available')
        
        return self.file_handler.load_proxies()
    
    def get_random_proxy(self):
        """Get a random proxy from the list."""
        proxy_list = self.get_proxy_list()
        if not proxy_list:
            return None
        return random.choice(proxy_list)
    
    def find_working_proxy(self, max_attempts=10):
        """Find a working proxy by testing random proxies."""
        proxy_list = self.get_proxy_list()
        if not proxy_list:
            return None
        
        attempts = 0
        while attempts < max_attempts and proxy_list:
            proxy = random.choice(proxy_list)
            result = self.validator.validate_proxy(proxy)
            
            if result['valid']:
                return result
            else:
                proxy_list = self.file_handler.remove_proxy(
                    proxy_list, proxy['IP_Address_td']
                )
                self.file_handler.save_proxies(proxy_list)
                logger.info(f"Removed invalid proxy: {result['proxy']}")
                attempts += 1
        
        return None
    
    def validate_all_proxies(self):
        """Validate all proxies in the list."""
        proxy_list = self.get_proxy_list()
        if not proxy_list:
            return []
        
        return self.validator.validate_proxy_list(proxy_list)
    
    def get_stats(self):
        """Get proxy data statistics."""
        return self.file_handler.get_file_stats()