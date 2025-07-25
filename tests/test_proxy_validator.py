#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Unit tests for proxy validator module."""

import unittest
from unittest.mock import Mock, patch
import ipaddress

from proxygenerator.core.proxy_validator import ProxyValidator


class TestProxyValidator(unittest.TestCase):
    """Test cases for ProxyValidator class."""
    
    def setUp(self):
        """Set up test environment."""
        self.validator = ProxyValidator(timeout=1)
    
    @patch('proxygenerator.core.proxy_validator.urlopen')
    @patch('proxygenerator.core.proxy_validator.install_opener')
    @patch('proxygenerator.core.proxy_validator.build_opener')
    def test_validate_proxy_success(self, mock_build_opener, mock_install_opener, mock_urlopen):
        """Test successful proxy validation."""
        proxy_info = {
            'IP_Address_td': '1.1.1.1',
            'Port_td': '8080'
        }
        
        mock_response = Mock()
        mock_response.read.return_value = b'192.168.1.1'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        mock_urlopen.return_value = mock_response
        
        result = self.validator.validate_proxy(proxy_info)
        
        self.assertTrue(result['valid'])
        self.assertEqual(result['proxy'], '1.1.1.1:8080')
        self.assertEqual(result['result_ip'], '192.168.1.1')
        self.assertEqual(result['original_info'], proxy_info)
    
    @patch('proxygenerator.core.proxy_validator.urlopen')
    @patch('proxygenerator.core.proxy_validator.install_opener')
    @patch('proxygenerator.core.proxy_validator.build_opener')
    def test_validate_proxy_failure(self, mock_build_opener, mock_install_opener, mock_urlopen):
        """Test proxy validation failure."""
        proxy_info = {
            'IP_Address_td': '1.1.1.1',
            'Port_td': '8080'
        }
        
        mock_urlopen.side_effect = ConnectionError("Connection timeout")
        
        result = self.validator.validate_proxy(proxy_info)
        
        self.assertFalse(result['valid'])
        self.assertEqual(result['proxy'], '1.1.1.1:8080')
        self.assertEqual(result['error'], 'Network error: Connection timeout')
        self.assertEqual(result['original_info'], proxy_info)
    
    def test_validate_proxy_list(self):
        """Test validating a list of proxies."""
        proxy_list = [
            {'IP_Address_td': '1.1.1.1', 'Port_td': '8080'},
            {'IP_Address_td': '2.2.2.2', 'Port_td': '3128'}
        ]
        
        with patch.object(self.validator, 'validate_proxy') as mock_validate:
            mock_validate.side_effect = [
                {'valid': True, 'proxy': '1.1.1.1:8080'},
                {'valid': False, 'proxy': '2.2.2.2:3128'}
            ]
            
            results = self.validator.validate_proxy_list(proxy_list)
            
            self.assertEqual(len(results), 2)
            self.assertTrue(results[0]['valid'])
            self.assertFalse(results[1]['valid'])
            self.assertEqual(mock_validate.call_count, 2)
    
    def test_validate_proxy_info_valid(self):
        """Test valid proxy info validation."""
        proxy_info = {
            'IP_Address_td': '8.8.8.8',
            'Port_td': '8080'
        }
        
        ip, port = self.validator._validate_proxy_info(proxy_info)
        self.assertEqual(ip, '8.8.8.8')
        self.assertEqual(port, 8080)
    
    def test_validate_proxy_info_invalid_ip(self):
        """Test invalid IP address validation."""
        proxy_info = {
            'IP_Address_td': '192.168.1.1',  # Private IP
            'Port_td': '8080'
        }
        
        with self.assertRaises(ValueError) as context:
            self.validator._validate_proxy_info(proxy_info)
        self.assertIn("private/loopback/reserved", str(context.exception))
    
    def test_validate_proxy_info_invalid_port(self):
        """Test invalid port validation."""
        proxy_info = {
            'IP_Address_td': '8.8.8.8',
            'Port_td': '99999'  # Port out of range
        }
        
        with self.assertRaises(ValueError) as context:
            self.validator._validate_proxy_info(proxy_info)
        self.assertIn("Port out of range", str(context.exception))
    
    def test_validate_proxy_info_missing_data(self):
        """Test missing IP or port validation."""
        proxy_info = {
            'IP_Address_td': '8.8.8.8'
            # Missing Port_td
        }
        
        with self.assertRaises(ValueError) as context:
            self.validator._validate_proxy_info(proxy_info)
        self.assertIn("Missing IP address or port", str(context.exception))
    
    def test_validate_proxy_with_invalid_info(self):
        """Test proxy validation with invalid info returns proper error."""
        proxy_info = {
            'IP_Address_td': '127.0.0.1',  # Loopback
            'Port_td': '8080'
        }
        
        result = self.validator.validate_proxy(proxy_info)
        
        self.assertFalse(result['valid'])
        self.assertIn('Validation error', result['error'])
        self.assertEqual(result['original_info'], proxy_info)


if __name__ == '__main__':
    unittest.main()