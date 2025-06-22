#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""Main entry point for the proxy generator application."""

import logging
import sys
from .core.proxy_manager import ProxyManager


def setup_logging(level=logging.INFO):
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main function that replicates the original proxy.py behavior."""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        manager = ProxyManager()

        # Get statistics about current data
        stats = manager.get_stats()
        logger.info("Current data stats: %s", stats)

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
            logger.info("Successfully found working proxy")
            return 0
        
        print("No working proxy found")
        logger.warning("No working proxy could be found")
        return 1
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        return 0
    except Exception as e:
        logger.error("Unexpected error in main: %s", e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
