#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Proxy validator module for testing proxy functionality."""

import asyncio
import ipaddress
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import ProxyHandler, build_opener, install_opener, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)


class ProxyValidator:
    """Handles proxy validation and testing."""

    def __init__(self, timeout=5):
        self.timeout = timeout
        # Use HTTP endpoint for broader proxy compatibility
        # Many proxies don't support HTTPS CONNECT tunneling
        self.test_url = 'http://ifconfig.co/ip'

    def _validate_proxy_info(self, proxy_info):
        """Validate proxy IP address and port before testing."""
        ip_address = proxy_info.get('IP_Address_td')
        port = proxy_info.get('Port_td')
        
        if not ip_address or not port:
            raise ValueError("Missing IP address or port")
        
        # Validate IP address format
        try:
            parsed_ip = ipaddress.ip_address(ip_address)
        except ValueError as e:
            raise ValueError(f"Invalid IP address format: {ip_address}") from e
        
        # Block private, loopback, and reserved addresses to prevent SSRF
        if parsed_ip.is_private or parsed_ip.is_loopback or parsed_ip.is_reserved:
            raise ValueError(f"Invalid IP address (private/loopback/reserved): {ip_address}")
        
        # Validate port range
        try:
            port_num = int(port)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid port format: {port}") from e
        
        if not (1 <= port_num <= 65535):
            raise ValueError(f"Port out of range (1-65535): {port}")
        
        return ip_address, port_num

    def validate_proxy(self, proxy_info):
        """Test if a proxy is working."""
        try:
            ip_address, port = self._validate_proxy_info(proxy_info)
            proxy_string = f"{ip_address}:{port}"
        except ValueError as e:
            logger.warning("Invalid proxy info: %s", e)
            return {
                'valid': False,
                'proxy': f"{proxy_info.get('IP_Address_td', 'unknown')}:{proxy_info.get('Port_td', 'unknown')}",
                'error': f'Validation error: {str(e)}',
                'original_info': proxy_info
            }

        logger.debug("Testing proxy: %s", proxy_string)

        # Build opener with HTTP proxy handler only for compatibility
        # Most free proxies don't support HTTPS CONNECT tunneling
        opener = build_opener(ProxyHandler({'http': proxy_string}))
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        install_opener(opener)

        try:
            with urlopen(self.test_url, timeout=self.timeout) as response:
                result_ip = response.read().decode('UTF-8').strip()
                logger.info("Proxy %s is working, external IP: %s", proxy_string, result_ip)
                return {
                    'valid': True,
                    'proxy': proxy_string,
                    'result_ip': result_ip,
                    'original_info': proxy_info
                }
        except (ConnectionError, TimeoutError) as e:
            logger.debug("Network error testing proxy %s: %s", proxy_string, e)
            return {
                'valid': False,
                'proxy': proxy_string,
                'error': f'Network error: {str(e)}',
                'original_info': proxy_info
            }
        except (URLError, HTTPError) as e:
            logger.debug("HTTP error testing proxy %s: %s", proxy_string, e)
            return {
                'valid': False,
                'proxy': proxy_string,
                'error': f'HTTP error: {str(e)}',
                'original_info': proxy_info
            }
        except UnicodeDecodeError as e:
            logger.warning("Decode error for proxy %s: %s", proxy_string, e)
            return {
                'valid': False,
                'proxy': proxy_string,
                'error': f'Decode error: {str(e)}',
                'original_info': proxy_info
            }

    def validate_proxy_list(self, proxy_list, max_workers=10):
        """Validate a list of proxies concurrently for better performance."""
        if not proxy_list:
            return []
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all validation tasks
            future_to_proxy = {
                executor.submit(self.validate_proxy, proxy): proxy 
                for proxy in proxy_list
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_proxy):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    proxy = future_to_proxy[future]
                    logger.error("Unexpected error validating proxy %s: %s", 
                               f"{proxy.get('IP_Address_td', 'unknown')}:{proxy.get('Port_td', 'unknown')}", e)
                    results.append({
                        'valid': False,
                        'proxy': f"{proxy.get('IP_Address_td', 'unknown')}:{proxy.get('Port_td', 'unknown')}",
                        'error': f'Unexpected error: {str(e)}',
                        'original_info': proxy
                    })
        
        return results
