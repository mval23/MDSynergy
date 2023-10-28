import streamlit as st
import pandas as pd
import yfinance as yf
import time

# Streamlit app title
st.title("Stock Price Alert System")

# Sidebar input for user-defined alerts
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL):")
target_price = st.sidebar.number_input("Set Target Price:")
refresh_rate = st.sidebar.number_input("Refresh Rate (seconds):")


# Function to check stock price
def check_stock_price(symbol, target):
    stock = yf.Ticker(symbol)
    stock_info = stock.history(period="1d")
    current_price = stock_info['Close'].iloc[-1]
    return current_price, current_price >= target


# Create an empty dataframe to store alerts
alerts_df = pd.DataFrame(columns=["Symbol", "Target Price", "Current Price", "Status"])


# Function to add an alert to the dataframe
def add_alert(symbol, target_price):
    current_price, status = check_stock_price(symbol, target_price)
    alerts_df.loc[len(alerts_df)] = [symbol, target_price, current_price, status]


# Streamlit loop
while True:
    st.write("Active Alerts:")
    st.write(alerts_df)

    if stock_symbol and target_price:
        add_alert(stock_symbol, target_price)

    time.sleep(refresh_rate)

## 2

elif selected == 'Financial Calculators':
    st.title("Financial Calculators")
    calculator_option = st.selectbox("Select a Calculator", ["Compound Interest Calculator", "ROI Calculator"])

    if calculator_option == "Compound Interest Calculator":
        st.subheader("Compound Interest Calculator")

        # Input fields for principal amount, interest rate, compounding frequency, and time period
        principal = st.number_input("Principal Amount", value=1000.0, step=1.0)
        interest_rate = st.number_input("Annual Interest Rate (%)", value=5.0, step=0.1)
        compounding_frequency = st.number_input("Compounding Frequency (per year)", value=1, step=1)
        time_period = st.number_input("Time Period (years)", value=5, step=1)

        # Calculate compound interest
        if st.button("Calculate"):
            compounded_amount = principal * (1 + (interest_rate / 100) / compounding_frequency) ** (compounding_frequency * time_period)
            st.write(f"Future Value: ${compounded_amount:.2f}")

    elif calculator_option == "ROI Calculator":
        st.subheader("ROI Calculator")

        # Input fields for initial investment, final value, and time period
        initial_investment = st.number_input("Initial Investment", value=10000.0, step=1.0)
        final_value = st.number_input("Final Value", value=15000.0, step=1.0)
        time_period = st.number_input("Time Period (years)", value=3, step=1)

        # Calculate ROI
        if st.button("Calculate"):
            roi = ((final_value - initial_investment) / initial_investment) * 100
            st.write(f"ROI: {roi:.2f}%")
# 2 .2

import streamlit as st
import yfinance as yf

# ... (your existing code)

elif selected == 'Financial Calculators':
    st.title("Financial Calculators")
    calculator_option = st.selectbox("Select a Calculator", ["Compound Interest Calculator", "ROI Calculator"])

    if calculator_option == "Compound Interest Calculator":
        st.subheader("Compound Interest Calculator")

        # Input fields for principal amount, interest rate, compounding frequency, and time period
        principal = st.number_input("Principal Amount", value=1000.0, step=1.0)
        interest_rate = st.number_input("Annual Interest Rate (%)", value=5.0, step=0.1)
        compounding_frequency = st.number_input("Compounding Frequency (per year)", value=1, step=1)
        time_period = st.number_input("Time Period (years)", value=5, step=1)

        # Select a stock for returns
        stock_symbol = st.text_input("Stock Symbol (e.g., AAPL for Apple Inc.)", value="AAPL")

        # Fetch stock data
        stock = yf.Ticker(stock_symbol)
        stock_data = stock.history(period=f"{time_period}y")

        if not stock_data.empty:
            # Calculate compound interest based on stock returns
            compounded_amount = principal
            for _, row in stock_data.iterrows():
                compounded_amount *= (1 + row['Close'] / row['Open'] - 1)

            # Display stock data
            st.write(f"Stock: {stock_symbol}")
            st.write(f"Initial Price: ${stock_data['Open'].iloc[0]:.2f}")
            st.write(f"Final Price: ${stock_data['Close'].iloc[-1]:.2f}")

            # Calculate compound interest
            compounded_amount = round(compounded_amount, 2)
            st.write(f"Future Value (with stock returns): ${compounded_amount:.2f}")

        else:
            st.warning("Stock data not found. Please enter a valid stock symbol.")

