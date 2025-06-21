#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Unit tests for file handler module."""

import json
import os
import tempfile
import time
import unittest
from unittest.mock import patch

from proxygenerator.utils.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    """Test cases for FileHandler class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.handler = FileHandler(self.temp_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_save_and_load_proxies(self):
        """Test saving and loading proxy data."""
        test_data = [
            {'IP_Address_td': '1.1.1.1', 'Port_td': '8080'},
            {'IP_Address_td': '2.2.2.2', 'Port_td': '3128'}
        ]
        
        # Test save
        result = self.handler.save_proxies(test_data)
        self.assertTrue(result)
        
        # Test load
        loaded_data = self.handler.load_proxies()
        self.assertEqual(loaded_data, test_data)
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        result = self.handler.load_proxies()
        self.assertEqual(result, [])
    
    def test_is_data_fresh(self):
        """Test data freshness checking."""
        # No file exists
        self.assertFalse(self.handler.is_data_fresh())
        
        # Create file
        test_data = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
        self.handler.save_proxies(test_data)
        
        # File is fresh
        self.assertTrue(self.handler.is_data_fresh())
        
        # File is old (simulate by setting max_age to 0)
        self.assertFalse(self.handler.is_data_fresh(max_age_seconds=0))
    
    def test_remove_proxy(self):
        """Test proxy removal from list."""
        proxy_list = [
            {'IP_Address_td': '1.1.1.1', 'Port_td': '8080'},
            {'IP_Address_td': '2.2.2.2', 'Port_td': '3128'},
            {'IP_Address_td': '3.3.3.3', 'Port_td': '8080'}
        ]
        
        result = self.handler.remove_proxy(proxy_list, '2.2.2.2')
        
        expected = [
            {'IP_Address_td': '1.1.1.1', 'Port_td': '8080'},
            {'IP_Address_td': '3.3.3.3', 'Port_td': '8080'}
        ]
        
        self.assertEqual(result, expected)
    
    def test_get_file_stats(self):
        """Test file statistics."""
        # No file
        stats = self.handler.get_file_stats()
        self.assertFalse(stats['exists'])
        self.assertEqual(stats['count'], 0)
        
        # With file
        test_data = [{'IP_Address_td': '1.1.1.1', 'Port_td': '8080'}]
        self.handler.save_proxies(test_data)
        
        stats = self.handler.get_file_stats()
        self.assertTrue(stats['exists'])
        self.assertEqual(stats['count'], 1)
        self.assertGreater(stats['size'], 0)
        self.assertIsNotNone(stats['modified'])


if __name__ == '__main__':
    unittest.main()