#!/usr/bin/env python3
"""Standalone script: clear the e-Paper display and exit.

Run from the project root:
    python clear_screen.py
"""
import sys
import os
import logging

from config import Config

lib_dir = Config.get_epaper_lib_path()
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)

from stock_ticker import StockTicker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    ticker = StockTicker()
    try:
        ticker.clear_screen()
    except Exception:
        logging.error("Failed to clear the display:", exc_info=True)
        sys.exit(1)
