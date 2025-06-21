#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Proxy validator module for testing proxy functionality."""

import logging
from urllib.request import ProxyHandler, build_opener, install_opener, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)


class ProxyValidator:
    """Handles proxy validation and testing."""
    
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.test_url = 'http://ifconfig.co/ip'
    
    def validate_proxy(self, proxy_info):
        """Test if a proxy is working."""
        ip_address = proxy_info['IP_Address_td']
        port = proxy_info['Port_td']
        proxy_string = f"{ip_address}:{port}"
        
        logger.debug(f"Testing proxy: {proxy_string}")
        
        opener = build_opener(ProxyHandler({'http': proxy_string}))
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        install_opener(opener)
        
        try:
            with urlopen(self.test_url, timeout=self.timeout) as response:
                result_ip = response.read().decode('UTF-8').strip()
                logger.info(f"Proxy {proxy_string} is working, external IP: {result_ip}")
                return {
                    'valid': True,
                    'proxy': proxy_string,
                    'result_ip': result_ip,
                    'original_info': proxy_info
                }
        except (ConnectionError, TimeoutError) as e:
            logger.debug(f"Network error testing proxy {proxy_string}: {e}")
            return {
                'valid': False,
                'proxy': proxy_string,
                'error': f'Network error: {str(e)}',
                'original_info': proxy_info
            }
        except (URLError, HTTPError) as e:
            logger.debug(f"HTTP error testing proxy {proxy_string}: {e}")
            return {
                'valid': False,
                'proxy': proxy_string,
                'error': f'HTTP error: {str(e)}',
                'original_info': proxy_info
            }
        except UnicodeDecodeError as e:
            logger.warning(f"Decode error for proxy {proxy_string}: {e}")
            return {
                'valid': False,
                'proxy': proxy_string,
                'error': f'Decode error: {str(e)}',
                'original_info': proxy_info
            }
    
    def validate_proxy_list(self, proxy_list):
        """Validate a list of proxies."""
        results = []
        for proxy in proxy_list:
            result = self.validate_proxy(proxy)
            results.append(result)
        return results