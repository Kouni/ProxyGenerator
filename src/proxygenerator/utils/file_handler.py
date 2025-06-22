#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""File handling utilities for proxy data management."""

import json
import logging
import os
import time
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class FileHandler:
    """Handles file operations for proxy data."""

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.proxy_file = os.path.join(data_dir, 'proxies.json')
        os.makedirs(data_dir, exist_ok=True)

    def save_proxies(self, proxy_list):
        """Save proxy list to JSON file with metadata."""
        try:
            now = datetime.now(timezone.utc)
            data = {
                "metadata": {
                    "generated_at": now.isoformat(),
                    "generated_timestamp": int(now.timestamp()),
                    "count": len(proxy_list),
                    "source": "free-proxy-list.net",
                    "format_version": "1.0"
                },
                "proxies": proxy_list
            }

            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Successfully saved %d proxies with metadata to %s", len(proxy_list), self.proxy_file)
            return True
        except OSError as e:
            logger.error("File I/O error saving proxies: %s", e)
            return False
        except (TypeError, ValueError) as e:
            logger.error("JSON serialization error: %s", e)
            return False

    def load_proxies(self):
        """Load proxy list from JSON file."""
        try:
            if not os.path.exists(self.proxy_file):
                logger.debug("Proxy file %s does not exist", self.proxy_file)
                return []

            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Handle new format with metadata
                if isinstance(data, dict) and 'proxies' in data:
                    proxies = data['proxies']
                    metadata = data.get('metadata', {})
                    logger.debug("Loaded %d proxies with metadata from %s", len(proxies), self.proxy_file)
                    logger.debug("Data generated at: %s", metadata.get('generated_at', 'unknown'))
                # Handle legacy format (list of proxies)
                elif isinstance(data, list):
                    proxies = data
                    logger.debug("Loaded %d proxies (legacy format) from %s", 
                                len(proxies), self.proxy_file)
                else:
                    logger.warning("Unknown data format in %s", self.proxy_file)
                    return []

                return proxies
        except OSError as e:
            logger.error("File I/O error loading proxies: %s", e)
            return []
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
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

    def get_metadata(self):
        """Get metadata from proxy file."""
        try:
            if not os.path.exists(self.proxy_file):
                return None

            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Return metadata if present
                if isinstance(data, dict) and 'metadata' in data:
                    return data['metadata']
                return None
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error reading metadata: %s", e)
            return None

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
