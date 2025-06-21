#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""File handling utilities for proxy data management."""

import json
import logging
import os
import time

logger = logging.getLogger(__name__)


class FileHandler:
    """Handles file operations for proxy data."""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.proxy_file = os.path.join(data_dir, 'proxies.json')
        os.makedirs(data_dir, exist_ok=True)
    
    def save_proxies(self, proxy_list):
        """Save proxy list to JSON file."""
        try:
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                json.dump(proxy_list, f, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved {len(proxy_list)} proxies to {self.proxy_file}")
            return True
        except OSError as e:
            logger.error(f'File I/O error saving proxies: {e}')
            return False
        except (TypeError, ValueError) as e:
            logger.error(f'JSON serialization error: {e}')
            return False
    
    def load_proxies(self):
        """Load proxy list from JSON file."""
        try:
            if not os.path.exists(self.proxy_file):
                logger.debug(f"Proxy file {self.proxy_file} does not exist")
                return []
            
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                proxies = json.load(f)
                logger.debug(f"Loaded {len(proxies)} proxies from {self.proxy_file}")
                return proxies
        except OSError as e:
            logger.error(f'File I/O error loading proxies: {e}')
            return []
        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error: {e}')
            return []
    
    def is_data_fresh(self, max_age_seconds=300):
        """Check if proxy data is fresh (newer than max_age_seconds)."""
        if not os.path.exists(self.proxy_file):
            return False
        
        file_age = time.time() - os.path.getmtime(self.proxy_file)
        return file_age < max_age_seconds
    
    def remove_proxy(self, proxy_list, ip_address):
        """Remove a proxy from the list by IP address."""
        updated_list = [
            proxy for proxy in proxy_list 
            if proxy.get('IP_Address_td') != ip_address
        ]
        return updated_list
    
    def get_file_stats(self):
        """Get statistics about the proxy file."""
        if not os.path.exists(self.proxy_file):
            return {'exists': False, 'count': 0, 'size': 0, 'modified': None}
        
        stat = os.stat(self.proxy_file)
        proxy_count = len(self.load_proxies())
        
        return {
            'exists': True,
            'count': proxy_count,
            'size': stat.st_size,
            'modified': stat.st_mtime
        }