import sys
import os
import logging

from config import Config
from stock_ticker import StockTicker

lib_dir = Config.get_epaper_lib_path()
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    ticker = StockTicker()
    try:
        ticker.run()
    except KeyboardInterrupt:
        ticker.cleanup()
    except Exception as e:
        logging.error("Unexpected error:", exc_info=True)
