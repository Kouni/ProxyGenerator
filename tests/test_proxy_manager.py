#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Unit tests for proxy manager module."""

import tempfile
import unittest
from unittest.mock import Mock, patch

from proxygenerator.core.proxy_manager import ProxyManager


class TestProxyManager(unittest.TestCase):
    """Test cases for ProxyManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ProxyManager(cache_dir=self.temp_dir, data_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_refresh_proxy_data_success(self):
        """Test successfully refreshing proxy data."""
        with patch.object(self.manager.fetcher, 'fetch_proxy_list') as mock_fetch, \
             patch.object(self.manager.fetcher, 'parse_proxy_list') as mock_parse, \
             patch.object(self.manager.file_handler, 'save_proxies') as mock_save:
            
            mock_fetch.return_value = '<html>test</html>'
            mock_parse.return_value = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
            mock_save.return_value = True
            
            result = self.manager.refresh_proxy_data()
            
            self.assertTrue(result)
            mock_fetch.assert_called_once()
            mock_parse.assert_called_once_with('<html>test</html>')
            mock_save.assert_called_once()
    
    def test_refresh_proxy_data_failure(self):
        """Test proxy data refresh failure."""
        with patch.object(self.manager.fetcher, 'fetch_proxy_list') as mock_fetch:
            mock_fetch.side_effect = ConnectionError("Network error")
            
            result = self.manager.refresh_proxy_data()
            
            self.assertFalse(result)
    
    def test_get_proxy_list_fresh_data(self):
        """Test getting proxy list with fresh data."""
        test_data = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
        
        with patch.object(self.manager.file_handler, 'is_data_fresh') as mock_fresh, \
             patch.object(self.manager.file_handler, 'load_proxies') as mock_load:
            
            mock_fresh.return_value = True
            mock_load.return_value = test_data
            
            result = self.manager.get_proxy_list()
            
            self.assertEqual(result, test_data)
            mock_fresh.assert_called_once()
            mock_load.assert_called_once()
    
    def test_get_proxy_list_stale_data(self):
        """Test getting proxy list with stale data."""
        test_data = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
        
        with patch.object(self.manager.file_handler, 'is_data_fresh') as mock_fresh, \
             patch.object(self.manager.file_handler, 'load_proxies') as mock_load, \
             patch.object(self.manager, 'refresh_proxy_data') as mock_refresh:
            
            mock_fresh.return_value = False
            mock_load.return_value = test_data
            mock_refresh.return_value = True
            
            result = self.manager.get_proxy_list()
            
            self.assertEqual(result, test_data)
            mock_refresh.assert_called_once()
    
    def test_get_random_proxy(self):
        """Test getting a random proxy."""
        test_data = [
            {'IP_Address_td': '1.1.1.1', 'Port_td': '8080'},
            {'IP_Address_td': '2.2.2.2', 'Port_td': '3128'}
        ]
        
        with patch.object(self.manager, 'get_proxy_list') as mock_get_list:
            mock_get_list.return_value = test_data
            
            result = self.manager.get_random_proxy()
            
            self.assertIn(result, test_data)
    
    def test_get_random_proxy_empty_list(self):
        """Test getting random proxy from empty list."""
        with patch.object(self.manager, 'get_proxy_list') as mock_get_list:
            mock_get_list.return_value = []
            
            result = self.manager.get_random_proxy()
            
            self.assertIsNone(result)
    
    def test_find_working_proxy_success(self):
        """Test finding a working proxy successfully."""
        test_data = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
        validation_result = {
            'valid': True,
            'proxy': '1.1.1.1:8080',
            'result_ip': '192.168.1.1'
        }
        
        with patch.object(self.manager, 'get_proxy_list') as mock_get_list, \
             patch.object(self.manager.validator, 'validate_proxy') as mock_validate:
            
            mock_get_list.return_value = test_data
            mock_validate.return_value = validation_result
            
            result = self.manager.find_working_proxy()
            
            self.assertEqual(result, validation_result)
    
    def test_find_working_proxy_no_valid_proxies(self):
        """Test finding working proxy when none are valid."""
        test_data = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
        validation_result = {
            'valid': False,
            'proxy': '1.1.1.1:8080',
            'error': 'Connection failed'
        }
        
        with patch.object(self.manager, 'get_proxy_list') as mock_get_list, \
             patch.object(self.manager.validator, 'validate_proxy') as mock_validate, \
             patch.object(self.manager.file_handler, 'remove_proxy') as mock_remove, \
             patch.object(self.manager.file_handler, 'save_proxies') as mock_save:
            
            mock_get_list.return_value = test_data
            mock_validate.return_value = validation_result
            mock_remove.return_value = []
            
            result = self.manager.find_working_proxy(max_attempts=1)
            
            self.assertIsNone(result)
            mock_remove.assert_called_once()
            mock_save.assert_called_once()
    
    def test_get_stats(self):
        """Test getting proxy statistics."""
        expected_stats = {
            'exists': True,
            'count': 10,
            'size': 1024,
            'modified': 1234567890
        }
        
        with patch.object(self.manager.file_handler, 'get_file_stats') as mock_stats:
            mock_stats.return_value = expected_stats
            
            result = self.manager.get_stats()
            
            self.assertEqual(result, expected_stats)


if __name__ == '__main__':
    unittest.main()