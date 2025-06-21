#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Unit tests for proxy fetcher module."""

import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open

from proxygenerator.core.proxy_fetcher import ProxyFetcher


class TestProxyFetcher(unittest.TestCase):
    """Test cases for ProxyFetcher class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.fetcher = ProxyFetcher(cache_dir=self.temp_dir, data_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('proxygenerator.core.proxy_fetcher.urlopen')
    def test_fetch_proxy_list_success(self, mock_urlopen):
        """Test successful proxy list fetching."""
        mock_response = Mock()
        mock_response.read.return_value = b'<html>test content</html>'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)
        mock_urlopen.return_value = mock_response
        
        result = self.fetcher.fetch_proxy_list()
        self.assertEqual(result, '<html>test content</html>')
        mock_urlopen.assert_called_once()
    
    @patch('proxygenerator.core.proxy_fetcher.urlopen')
    def test_fetch_proxy_list_error_with_cache(self, mock_urlopen):
        """Test fetching with error but cache available."""
        mock_urlopen.side_effect = ConnectionError("Network error")
        
        # Create cache file
        cache_file = f"{self.temp_dir}/proxies.html"
        with open(cache_file, 'w') as f:
            f.write('<html>cached content</html>')
        
        result = self.fetcher.fetch_proxy_list()
        self.assertEqual(result, '<html>cached content</html>')
    
    def test_parse_proxy_list(self):
        """Test parsing HTML content to proxy list."""
        html_content = '''
        <html>
            <tbody>
                <tr>
                    <td>1.1.1.1</td>
                    <td>8080</td>
                    <td>US</td>
                    <td>United States</td>
                    <td>anonymous</td>
                    <td>yes</td>
                    <td>yes</td>
                    <td>1 minute ago</td>
                </tr>
                <tr>
                    <td>2.2.2.2</td>
                    <td>3128</td>
                    <td>GB</td>
                    <td>United Kingdom</td>
                    <td>elite proxy</td>
                    <td>no</td>
                    <td>no</td>
                    <td>5 minutes ago</td>
                </tr>
            </tbody>
        </html>
        '''
        
        result = self.fetcher.parse_proxy_list(html_content)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['IP_Address_td'], '1.1.1.1')
        self.assertEqual(result[0]['Port_td'], '8080')
        self.assertEqual(result[1]['IP_Address_td'], '2.2.2.2')
        self.assertEqual(result[1]['Port_td'], '3128')
    
    def test_parse_proxy_list_no_tbody(self):
        """Test parsing HTML with no tbody element."""
        html_content = '<html><body>No table here</body></html>'
        
        result = self.fetcher.parse_proxy_list(html_content)
        self.assertEqual(result, [])
    
    def test_parse_proxy_list_incomplete_rows(self):
        """Test parsing HTML with incomplete table rows."""
        html_content = '''
        <html>
            <tbody>
                <tr>
                    <td>1.1.1.1</td>
                    <td>8080</td>
                </tr>
            </tbody>
        </html>
        '''
        
        result = self.fetcher.parse_proxy_list(html_content)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()