# Input field for stock symbol
stock_symbol = st.text_input("Stock Symbol (e.g., AAPL for Apple Inc.)", "AAPL")

# Create a figure for the live stock chart
fig: Figure = px.line(title=f"{stock_symbol} Live Stock Chart")

# Create an empty element for the live chart
chart_container = st.empty()

# Initialize variables for stock data and highlights
stock_data = None
stock_highlights = {}


# Function to update the live chart

def live_chart_data(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1d", interval="5m")
    def update_live_chart():

        if not stock_data.empty:

            # Clear the previous data
            fig.data = []

            # Update the live chart
            fig.add_scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name=f"{stock_symbol} Price")
            chart_container.plotly_chart(fig, use_container_width=True)


    # Show highlights or key information
    st.subheader("Stock Highlights")

    while True:

        # Refresh the chart every 5 seconds
        st.text("Updating live chart every 5 seconds...")
        update_live_chart()

        if stock_data is not None and not stock_data.empty:
            stock_highlights["Stock Symbol"] = stock_symbol
            stock_highlights["Last Trading Day"] = stock_data.index[-1].date()
            stock_highlights["Latest Price"] = f"${stock_data['Close'].iloc[-1]:.2f}"
            stock_highlights["High Price"] = f"${stock_data['High'].max():.2f}"
            stock_highlights["Low Price"] = f"${stock_data['Low'].min():.2f}"

            for key, value in stock_highlights.items():
                st.write(f"{key}: {value}")

        time.sleep(5)
        st.experimental_rerun()

    # Clear the live chart when not refreshing
    chart_container.empty()


ticker_list = ["AAPL", "GOOGL", "MSFT"]
def show_live_stock_charts(tickers):
    for t in tickers:
        live_chart_data()
################################################

import streamlit as st
import yfinance as yf
import plotly.express as px
import time

# Custom CSS to add rounded borders
css = """
<style>
.row-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #f1f1f1;
    margin: 10px 0;
    border-radius: 10px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
.column-text {
    width: 48%;
}
.column-chart {
    width: 48%;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1d", interval="5m")
    return stock_data


def create_live_stock_chart(ticker, stock_data):
    fig = px.line(title=f"{ticker} Live Stock Chart")

    if not stock_data.empty:
        # Create a live chart
        fig.add_scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name=f"{ticker} Price")

        # Display the live chart
        st.plotly_chart(fig, use_container_width=True)


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


# Example usage
ticker_list = ["AAPL", "GOOGL", "MSFT"]

# Iterate through tickers and organize content into rows with two columns
for ticker in ticker_list:
    stock_data = fetch_stock_data(ticker)

    # Create a row container with two columns
    col1, col2 = st.columns(2)

    # Display text in the first column
    with col1:
        display_stock_highlights(ticker, stock_data)

    # Display the live chart in the second column
    with col2:
        create_live_stock_chart(ticker, stock_data)

# Refresh data every 10 seconds (this code block will rerun indefinitely)
while True:
    time.sleep(10)
    for ticker in ticker_list:
        stock_data = fetch_stock_data(ticker)
        create_live_stock_chart(ticker, stock_data)

################################################
