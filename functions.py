import json
import threading
import time
from datetime import datetime

import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image, ImageDraw, ImageOps


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


def plot_multiple_stock_prices(tickers):
    """
    Plots the stock prices of multiple tickers on the same graph.
    :param tickers: list of str - list of stock ticker symbols
    """

    plt.figure(figsize=(12, 6))

    for ticker in tickers:
        data = yf.Ticker(ticker).history(period='1y')
        plt.plot(data.index, data['Close'], label=ticker)

    plt.title('Stock Prices Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.legend()
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()


# Stock Alert Functions
# def get_stock_symbol_using_chatgpt(company_name):
#     prompt = f"Find the stock symbol for the company {company_name}."
#     response = openai.Completion.create(
#       engine="text-davinci-003",
#       prompt=prompt,
#       max_tokens=100
#     )
#     return response['choices'][0]['text'].strip()

def get_current_stock_price(symbol):
    """
    Obtains the actual price of a Stock
    :param symbol: Stock symbol in the Stock Exchange
    """
    stock = yf.Ticker(symbol)
    return stock.history(period="1d")["Close"].iloc[-1]


def check_price_alert(symbol, target_price, current_price, up_down):
    """
    Verifies if the price beats the defined limits
    :param symbol: Stock symbol in the Stock Exchange
    :param target_price: Target price to compare with
    :param current_price: Current price to be comparable
    :param up_down: Checkings
    """
    if up_down:
        if current_price > target_price:
            return f"¡Alerta! El precio de {symbol} ha superado {target_price}"
        else:
            return None
    else:
        if current_price < target_price:
            return f"¡Alerta! El precio de {symbol} ha caído por debajo de {target_price}"
        else:
            return None


# Graphics Functions of Stock Alerts
# def create_live_stock_chart(ticker):
#     fig = px.line(title=f"{ticker} Live Stock Chart")
#     st.plotly_chart(fig, use_container_width=True)
#     return fig


# Function to create a live stock chart with a horizontal line at the target price
def create_live_stock_chart(ticker, stock_data):
    fig = go.Figure()

    fig.update_layout(title=f"{ticker} Live Stock Chart")

    # Add a scatter plot for stock data
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Stock Price'))

    st.plotly_chart(fig, use_container_width=True)

    return fig


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1d", interval="5m")
    return stock_data


# Function to update the live stock chart with new data
# def update_live_stock_chart(ticker, stock_data, fig):
#     if not stock_data.empty:
#         # Actualizar el gráfico con los nuevos datos
#         fig.data[0].x = stock_data.index
#         fig.data[0].y = stock_data['Close']
#
#         # Restablecer la escala del eje Y para ajustarse a los nuevos datos
#         fig.update_yaxes(range=[stock_data['Close'].min(), stock_data['Close'].max()])
#
#     return fig

def update_live_stock_chart(ticker, stock_data, fig):
    if not stock_data.empty:
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Stock Price")
        fig.update_traces(x=stock_data.index, y=stock_data["Close"], name=ticker)


def display_stock_highlights(ticker, stock_data):
    st.subheader(f"Stock Highlights for {ticker}")

    if not stock_data.empty:
        last_trading_day = stock_data.index[-1].date()
        latest_price = f"${stock_data['Close'].iloc[-1]:.2f}"
        high_price = f"${stock_data['High'].max():.2f}"
        low_price = f"${stock_data['Low'].min():.2f}"

        st.write(f"Stock Symbol: {ticker}")
        st.write(f"Last Trading Day: {last_trading_day}")
        st.write(f"Latest Price: {latest_price}")
        st.write(f"High Price: {high_price}")
        st.write(f"Low Price: {low_price}")


# Additional Functions

# Función para aplicar transparencia a los bordes de la imagen
def apply_transparency(image_path, border_size):
    original_image = Image.open(image_path).convert("RGBA")
    transparent_image = Image.new("RGBA", original_image.size, (0, 0, 0, 0))

    mask = Image.new("L", original_image.size, 0)
    draw = ImageDraw.Draw(mask)

    draw.rectangle([border_size, border_size, original_image.width - border_size, original_image.height - border_size],
                   fill=255)

    transparent_image.paste(original_image, (0, 0), mask)

    return transparent_image
