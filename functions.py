import json
from datetime import datetime

import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

# Functions

def get_stock_price(ticker):
    """
    Returns the current stock price of the ticker
    :param ticker: str - ticker of the stock

    """
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1].Close)


def calculate_SMA(ticker, window):
    """
    Media Móvil Simple(SMA)
    Returns the Simple Moving Average of the ticker
    :param ticker: str - ticker of the stock
    :param window: int - window of the SMA

    """
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])


def calculate_EMA(ticker, window):
    """
    Media Móvil Exponencial
    Returns the Simple Moving Average of the ticker
    :param ticker: str - ticker of the stock
    :param window: int - window of the SMA

    """
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])


def calculate_RSI(ticker, window):
    """
    Returns the Simple Moving Average of the ticker
    :param ticker: str - ticker of the stock
    :param window: int - window of the SMA

    """
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14 - 1, adjust=False).mean()
    ema_down = down.ewm(com=14 - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs.iloc[-1])))


def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal
    return f'MACD: {MACD.iloc[-1]}, Signal: {signal.iloc[-1]}, MACD Histogram: {MACD_histogram.iloc[-1]}'


def plot_stock_price(ticker):
    """
    Plots the stock price of the ticker
    :param ticker: str - ticker of the stock

    """
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()


# def calculate_Bollinger_Bands(ticker, window, num_std_dev):
#     """
#     Calculates the Bollinger Bands for a given stock.
#     :param ticker: str - ticker of the stock
#     :param window: int - window for calculating the moving average
#     :param num_std_dev: int - number of standard deviations for the bands
#     :return: Tuple (upper_band, middle_band, lower_band)
#     """
#     data = yf.Ticker(ticker).history(period='1y').Close
#     middle_band = data.rolling(window=window).mean()
#     std_dev = data.rolling(window=window).std()
#     upper_band = middle_band + num_std_dev * std_dev
#     lower_band = middle_band - num_std_dev * std_dev
#     return upper_band.iloc[-1], middle_band.iloc[-1], lower_band.iloc[-1]
#
#
# def plot_multiple_stock_prices(tickers):
#     """
#     Plots the historical stock prices of multiple tickers for the current year.
#     :param tickers: List of stock ticker symbols (e.g., ['AAPL', 'MSFT'])
#     """
#     # Calculate the current year's start and end dates
#     current_year = datetime.now().year
#     start_date = f"{current_year}-01-01"
#     end_date = f"{current_year}-12-31"
#
#     # Fetch historical data for each ticker for the current year
#     data = yf.download(tickers, start=start_date, end=end_date)
#
#     # Create a plot
#     plt.figure(figsize=(10, 5))
#
#     # Plot the stock prices for each ticker
#     for ticker in tickers:
#         plt.plot(data.index, data['Adj Close'][ticker], label=ticker)
#
#     # Set labels and title
#     plt.xlabel('Date')
#     plt.ylabel('Stock Price')
#     plt.title(f'Stock Prices for {current_year}')
#
#     # Add a legend
#     plt.legend(tickers)
#
#     # Show the plot
#     plt.grid(True)
#     plt.show()
