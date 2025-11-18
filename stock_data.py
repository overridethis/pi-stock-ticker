# -*- coding:utf-8 -*-
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, time as dtime


def get_stock_info(ticker):
    """
    Fetch current stock information including name, price, change percentage, and currency.

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        dict: Dictionary containing name, price, change_percent, and currency
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    name = info.get("shortName", ticker)
    price = info.get("regularMarketPrice", 0)
    change_percent = info.get("regularMarketChangePercent", 0)
    currency = info.get("currency", "USD")
    return {
        "name": name,
        "price": price,
        "change_percent": change_percent,
        "currency": currency
    }


def is_trading_day(ticker):
    """
    Check if today is a trading day for the given ticker.

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        bool: True if today is a trading day, False otherwise
    """
    try:
        stock = yf.Ticker(ticker)
        today = datetime.now().date()
        hist = stock.history(period="7d", interval="1d")
        return today in hist.index.date
    except Exception as e:
        logging.warning(f"Could not determine if today is a trading day: {e}")
        return False


def get_intraday_prices(ticker, open_time, close_time):
    """
    Fetch intraday prices at 5-minute intervals for the given ticker.

    Args:
        ticker (str): Stock ticker symbol
        open_time (time): Market open time
        close_time (time): Market close time

    Returns:
        pd.Series: Time series of closing prices at 5-minute intervals
    """
    stock = yf.Ticker(ticker)
    raw_df = stock.history(period="1d", interval="5m", prepost=False)

    if raw_df.empty:
        return pd.Series(dtype='float64')

    if raw_df.index.tz is None:
        raw_df.index = raw_df.index.tz_localize("America/New_York")

    raw_df.index = raw_df.index.tz_convert("Europe/Stockholm")
    raw_df.index = raw_df.index.tz_localize(None)
    raw_df.index = raw_df.index.map(lambda t: t.replace(second=0, microsecond=0))

    today = datetime.now().date()
    cet_open = datetime.combine(today, open_time)
    cet_close = datetime.combine(today, close_time)
    full_index = pd.date_range(start=cet_open, end=cet_close, freq="5min")

    full_series = pd.Series(index=full_index, dtype='float64')
    actual_close = raw_df['Close']
    actual_close = actual_close[~actual_close.index.duplicated(keep='last')]

    aligned = full_series.combine_first(actual_close)
    return aligned
