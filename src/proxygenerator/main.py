#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Main entry point for the proxy generator application."""

from .core.proxy_manager import ProxyManager


def main():
    """Main function that replicates the original proxy.py behavior."""
    manager = ProxyManager()
    
    # Get statistics about current data
    stats = manager.get_stats()
    
    # Check if we need to refresh data (similar to original logic)
    if not stats['exists'] or not manager.file_handler.is_data_fresh() or stats['count'] == 0:
        print("Refreshing proxy data...")
        manager.refresh_proxy_data()
    
    # Find a working proxy
    print("Finding working proxy...")
    result = manager.find_working_proxy()
    
    if result:
        # Get final statistics
        final_stats = manager.get_stats()
        print(f"Number of data records: {final_stats['count']}")
        print(f"Result: {result['result_ip']}:{result['proxy'].split(':')[1]}")
    else:
        print("No working proxy found")


if __name__ == '__main__':
    main()