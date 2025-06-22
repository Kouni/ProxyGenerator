#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Unit tests for main module."""

import logging
import sys
import unittest
from unittest.mock import Mock, patch, call

from proxygenerator.main import main, setup_logging


class TestMain(unittest.TestCase):
    """Test cases for main module functions."""
    
    def test_setup_logging(self):
        """Test logging setup configuration."""
        with patch('logging.basicConfig') as mock_config:
            setup_logging(logging.DEBUG)
            
            mock_config.assert_called_once()
            args, kwargs = mock_config.call_args
            
            self.assertEqual(kwargs['level'], logging.DEBUG)
            self.assertIn('%(asctime)s', kwargs['format'])
            self.assertIn('%(name)s', kwargs['format'])
            self.assertIn('%(levelname)s', kwargs['format'])
            self.assertIn('%(message)s', kwargs['format'])
            self.assertEqual(len(kwargs['handlers']), 1)
    
    @patch('proxygenerator.main.ProxyManager')
    @patch('proxygenerator.main.setup_logging')
    @patch('builtins.print')
    def test_main_success_with_existing_data(self, mock_print, mock_setup_logging, mock_manager_class):
        """Test main function with existing fresh data."""
        # Setup mock manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.get_stats.return_value = {
            'exists': True, 'count': 100, 'size': 1000, 'modified': 1234567890
        }
        mock_manager.file_handler.is_data_fresh.return_value = True
        mock_manager.find_working_proxy.return_value = {
            'valid': True,
            'proxy': '1.1.1.1:8080',
            'result_ip': '192.168.1.1'
        }
        
        main()
        
        # Verify calls
        mock_setup_logging.assert_called_once()
        mock_manager.get_stats.assert_called()
        mock_manager.file_handler.is_data_fresh.assert_called_once()
        mock_manager.find_working_proxy.assert_called_once()
        
        # Verify print calls
        expected_prints = [
            call("Finding working proxy..."),
            call("Number of data records: 100"),
            call("Result: 192.168.1.1:8080")
        ]
        mock_print.assert_has_calls(expected_prints)
    
    @patch('proxygenerator.main.ProxyManager')
    @patch('proxygenerator.main.setup_logging')
    @patch('builtins.print')
    def test_main_success_with_refresh(self, mock_print, mock_setup_logging, mock_manager_class):
        """Test main function that needs to refresh data."""
        # Setup mock manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.get_stats.side_effect = [
            {'exists': False, 'count': 0, 'size': 0, 'modified': None},
            {'exists': True, 'count': 50, 'size': 500, 'modified': 1234567890}
        ]
        mock_manager.file_handler.is_data_fresh.return_value = False
        mock_manager.refresh_proxy_data.return_value = True
        mock_manager.find_working_proxy.return_value = {
            'valid': True,
            'proxy': '2.2.2.2:3128',
            'result_ip': '192.168.1.2'
        }
        
        main()
        
        # Verify refresh was called
        mock_manager.refresh_proxy_data.assert_called_once()
        
        # Verify print calls
        expected_prints = [
            call("Refreshing proxy data..."),
            call("Finding working proxy..."),
            call("Number of data records: 50"),
            call("Result: 192.168.1.2:3128")
        ]
        mock_print.assert_has_calls(expected_prints)
    
    @patch('proxygenerator.main.ProxyManager')
    @patch('proxygenerator.main.setup_logging')
    @patch('builtins.print')
    def test_main_no_working_proxy(self, mock_print, mock_setup_logging, mock_manager_class):
        """Test main function when no working proxy is found."""
        # Setup mock manager
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager
        mock_manager.get_stats.return_value = {
            'exists': True, 'count': 10, 'size': 100, 'modified': 1234567890
        }
        mock_manager.file_handler.is_data_fresh.return_value = True
        mock_manager.find_working_proxy.return_value = None
        
        result = main()
        
        # Verify return code is 1 (error)
        self.assertEqual(result, 1)
        
        # Verify error message was printed
        mock_print.assert_any_call("No working proxy found")
    
    @patch('proxygenerator.main.ProxyManager')
    @patch('proxygenerator.main.setup_logging')
    def test_main_keyboard_interrupt(self, mock_setup_logging, mock_manager_class):
        """Test main function handles keyboard interrupt gracefully."""
        # Setup mock manager to raise KeyboardInterrupt
        mock_manager_class.side_effect = KeyboardInterrupt()
        
        result = main()
        
        # Verify return code is 0 (success)
        self.assertEqual(result, 0)
    
    @patch('proxygenerator.main.ProxyManager')
    @patch('proxygenerator.main.setup_logging')
    def test_main_unexpected_error(self, mock_setup_logging, mock_manager_class):
        """Test main function handles unexpected errors."""
        # Setup mock manager to raise exception
        mock_manager_class.side_effect = ConnectionError("Unexpected error")
        
        result = main()
        
        # Verify return code is 1 (error)
        self.assertEqual(result, 1)
    
    def test_main_logging_messages(self):
        """Test that appropriate log messages are generated."""
        with patch('proxygenerator.main.ProxyManager') as mock_manager_class, \
             patch('proxygenerator.main.setup_logging'), \
             patch('builtins.print'), \
             patch('logging.getLogger') as mock_get_logger:
            
            # Setup mock logger
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger
            
            # Setup mock manager
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            mock_manager.get_stats.return_value = {
                'exists': True, 'count': 100, 'size': 1000, 'modified': 1234567890
            }
            mock_manager.file_handler.is_data_fresh.return_value = True
            mock_manager.find_working_proxy.return_value = {
                'valid': True,
                'proxy': '1.1.1.1:8080',
                'result_ip': '192.168.1.1'
            }
            
            main()
            
            # Verify logger calls
            mock_logger.info.assert_any_call("Current data stats: %s", {'exists': True, 'count': 100, 'size': 1000, 'modified': 1234567890})
            mock_logger.info.assert_any_call("Successfully found working proxy")


if __name__ == '__main__':
    unittest.main()