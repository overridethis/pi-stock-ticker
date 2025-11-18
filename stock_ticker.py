# /usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, time as dtime
from PIL import Image, ImageDraw, ImageFont
import pytz

from waveshare_epd import epd3in52
from stock_data import get_stock_info, is_trading_day, get_intraday_prices
from config import Config

# -------------------------------------
# Helper Functions
# -------------------------------------

def market_is_closed(prices, ticker):
    """
    Determine if the market is currently closed.

    Args:
        prices (pd.Series): Time series of intraday prices
        ticker (str): Stock ticker symbol

    Returns:
        bool: True if market is closed (weekend, holiday, or no prices available)
    """
    # Weekend check
    if datetime.now().weekday() >= 5:
        return True
    # Holiday / no market session
    if not is_trading_day(ticker):
        return True
    # No intraday prices
    return prices.dropna().empty

def get_trading_hours(ticker):
    """
    Get trading hours based on the ticker's market.

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        tuple: (open_time, close_time) as time objects in CET/Stockholm timezone
    """
    if ticker.endswith(".ST") or ticker.upper() == "^OMX":
        return dtime(9, 0), dtime(17, 30)
    else:
        return dtime(15, 30), dtime(22, 0)

def get_currency_symbol(code):
    """
    Convert currency code to its symbol.

    Args:
        code (str): Three-letter currency code (e.g., 'USD', 'EUR')

    Returns:
        str: Currency symbol or the original code if not found
    """
    currency_map = {
        "USD": "$",
        "EUR": "\u20AC",
        "SEK": "kr",
        "NOK": "kr",
        "DKK": "kr",
        "GBP": "\u00A3",
        "CAD": "$",
        "JPY": "\u00A5",
        "CHF": "Fr",
        "CNY": "\u00A5",
        "INR": "\u20B9",
        "AUD": "$",
        "ZAR": "R"
    }
    return currency_map.get(code, code)

def create_price_plot(prices, filename="graph.png"):
    """
    Create an intraday price chart and save as a 1-bit black and white image.

    Args:
        prices (pd.Series): Time series of prices indexed by datetime
        filename (str): Output filename for the chart image (default: "graph.png")
    """
    fig, ax = plt.subplots(figsize=(3.4, 1.5), dpi=100)
    ax.set_xlim(prices.index[0], prices.index[-1])
    ax.fill_between(prices.index, prices.values, color="#BBBBBB", step="pre", where=~prices.isna())
    ax.plot(prices.index, prices.values, color="black", linewidth=1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.tick_params(axis='x', labelsize=6, rotation=0)
    ax.tick_params(axis='y', labelleft=False)
    valid = prices.dropna()
    if not valid.empty:
        ax.set_ylim(valid.min()*0.997, valid.max()*1.003)
    plt.grid(True, which='major', axis='x', linestyle='--', linewidth=0.3)
    plt.tight_layout(pad=0.5)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()
    image = Image.open(filename).convert('L')
    image = image.convert('1')
    image.save(filename)


# -------------------------------------
# StockTicker Class
# -------------------------------------

class StockTicker:
    """Stock ticker display for e-Paper screen."""

    def __init__(self):
        """Initialize the stock ticker with display and fonts."""
        self._epd = epd3in52.EPD()
        self._font24 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        self._font18 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
        self._font12 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
        self._tickers = Config.get_tickers()
        self._ticker_index = 0

    def run(self):
        """
        Main loop to display stock information.

        Initializes the e-Paper display and continuously cycles through configured
        stock tickers, updating the display with current price information and charts.
        """
        logging.info("epd3in52 Stock Ticker Started")
        self._epd.init()
        self._epd.send_command(0x50)
        self._epd.send_data(0x17)

        while True:
            ticker = self._tickers[self._ticker_index]
            logging.info(f"Updating stock data for {ticker} at {time.strftime('%H:%M:%S')}")
            open_time, close_time = get_trading_hours(ticker)

            try:
                data = get_stock_info(ticker)
                prices = get_intraday_prices(ticker, open_time, close_time)
                Himage = Image.new('1', (self._epd.height, self._epd.width), 255)
                draw = ImageDraw.Draw(Himage)

                is_index = ticker.startswith("^")
                postfix_currencies = ["SEK", "NOK", "DKK"]

                if is_index:
                    price_str = f"{data['price']:.2f}"
                elif data['currency'] in postfix_currencies:
                    price_str = f"{data['price']:.2f} {get_currency_symbol(data['currency'])}"
                else:
                    price_str = f"{get_currency_symbol(data['currency'])}{data['price']:.2f}"

                draw.text((10, 10), f"{data['name'][:10]}", font=self._font18, fill=0)
                draw.text((175, 10), price_str, font=self._font18, fill=0)
                draw.text((270, 10), f"({data['change_percent']:+.2f}%)", font=self._font18, fill=0)
                draw.line((10, 35, 350, 35), fill=0)
                draw.text((10, 40), 'INTRA DAY', font=self._font12, fill=0)

                if market_is_closed(prices, ticker):
                    closed_text = "Market is closed"
                    bbox = draw.textbbox((0, 0), closed_text, font=self._font18)
                    text_width = bbox[2] - bbox[0]
                    x = (self._epd.height - text_width) // 2
                    y = 100
                    draw.text((x, y), closed_text, font=self._font18, fill=0)

                else:
                    create_price_plot(prices)
                    graph_img = Image.open("graph.png").convert("1")
                    graph_resized = graph_img.resize((340, 155))
                    Himage.paste(graph_resized, (10, 60))


                stockholm_time = datetime.now(pytz.timezone("Europe/Stockholm"))
                draw.text((10, 220), f'Last sync: {stockholm_time.strftime("%Y-%m-%d %H:%M")}', font=self._font12, fill=0)

                self._epd.display(self._epd.getbuffer(Himage.rotate(180)))
                self._epd.lut_GC()
                self._epd.refresh()

                logging.info(f"Displayed {ticker}. Waiting 5 minutes...\n")

            except Exception as e:
                logging.error(f"Error fetching/displaying {ticker}: {e}")

            self._ticker_index = (self._ticker_index + 1) % len(self._tickers)
            time.sleep(Config.get_update_frequency())

    def cleanup(self):
        """
        Clean up resources and shut down the display.

        Clears the e-Paper display, puts it to sleep, and exits the GPIO module.
        """
        logging.info("Exiting on user request...")
        self._epd.Clear()
        self._epd.sleep()
        epd3in52.epdconfig.module_exit(cleanup=True)


# -------------------------------------
# Main
# -------------------------------------

if __name__ == "__main__":
    ticker = StockTicker()
    try:
        ticker.run()
    except KeyboardInterrupt:
        ticker.cleanup()
    except Exception as e:
        logging.error("Unexpected error:", exc_info=True)
