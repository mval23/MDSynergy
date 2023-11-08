import numpy as np
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
from plotly.graph_objs import Figure


from chatgpt import *

selected = "Home"

# Creación del título
st.set_page_config(page_title="MDSynergy")

# Inicialización de stocks en la sesión si no existe
if 'stocks' not in st.session_state:
    st.session_state.stocks = []

# if 'messages' not in st.session_state:
#     history = st.session_state['messages']

# 1. as sidebar menu
with st.sidebar:
    # Define a custom style for the option menu to make the background transparent
    custom_style = {"container": {"background-color": "transparent"},
                    "nav-link-selected": {"background-color": "transparent"}, }

    selected = option_menu("Menu", ["Home", 'MD Stockbot', "Prediction", "Historic", "Alert System", "Tests"],
                           icons=['house', 'chat-left-dots-fill', 'bar-chart-line', 'clock', 'exclamation-triangle-fill', 'bug'],
                           menu_icon="-dots", default_index=1, styles=custom_style)

if selected == 'Home':
    # Display the content for MD Synergy
    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
                <h1>MD Synergy</h1>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 2vh;'>
                <br>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
                <h3>by MDSynergy</h3>
            </div>
            """, unsafe_allow_html=True)
    st.write("Welcome to the MD Synergy page.")  # TODO: add content - David

elif selected == 'MD Stockbot':
    current_message = {'input': None, 'content': None, 'img': None}
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
        st.session_state.session_history = []
        st.session_state.session_history_2 = []

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
            <h1>Stock Analysis Chatbot Assistant</h1>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 2vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
            <h3>by MDSynergy</h3>
        </div>
        """, unsafe_allow_html=True)

    # st.markdown('by MDSynergy')

    user_input = st.text_input('Your input:')
    current_message['input'] = user_input

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 2vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)

    if user_input:
        try:
            st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})

            response = openai.ChatCompletion.create(model='gpt-3.5-turbo-0613', messages=st.session_state['messages'],
                                                    functions=functions, function_call='auto')

            response_message = response['choices'][0]['message']

            if response_message.get('function_call'):
                function_name = response_message['function_call']['name']
                function_args = json.loads(response_message['function_call']['arguments'])
                if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                    args_dict = {'ticker': function_args.get('ticker')}
                elif function_name in ['calculate_SMA', 'calculate_EMA']:
                    args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}
                elif function_name in ['plot_multiple_stock_prices']:
                    args_dict = {'tickers': function_args.get('tickers')}
                elif function_name in ['calculate_Bollinger_Bands']:
                    args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window'), 'num_std_dev': function_args.get('num_std_dev')}

                function_to_call = available_functions[function_name]
                function_response = function_to_call(**args_dict)

                if function_name == 'plot_stock_price' or function_name == 'plot_multiple_stock_prices':
                    st.image('stock.png')
                    image = Image.open('stock.png')  # Replace 'your_image.png' with your image file path
                    image_array = np.array(image)
                    current_message['img'] = image_array


                else:
                    st.session_state['messages'].append(response_message)
                    st.session_state['messages'].append(
                        {'role': 'function', 'name': function_name, 'content': function_response})
                    second_response = openai.ChatCompletion.create(model='gpt-3.5-turbo-0613',
                                                                   messages=st.session_state['messages'])
                    message = second_response['choices'][0]['message']['content']
                    st.markdown("""
                                            <style>
                                            .paragraph-section {
                                                padding: 20px;
                                                border-radius: 5px;
                                            }
                                            </style>
                                            """, unsafe_allow_html=True, )
                    st.markdown(f"""
                                                <div class="paragraph-section">
                                                    {message}
                                                </div>
                                                """, unsafe_allow_html=True, )
                    st.session_state['messages'].append(
                        {'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
                    current_message['content'] = message

            else:
                message = response_message['content']
                st.markdown("""
                                                        <style>
                                                        .paragraph-section {
                                                            padding: 20px;
                                                            border-radius: 5px;
                                                        }
                                                        </style>
                                                        """, unsafe_allow_html=True, )
                st.markdown(f"""
                                                            <div class="paragraph-section">
                                                                {message}
                                                            </div>
                                                            """, unsafe_allow_html=True, )
                current_message['content'] = message
                st.session_state['messages'].append({'role': 'assistant', 'content': response_message['content']})
            st.session_state.session_history.append(current_message)
            st.session_state.session_history_2.insert(0, current_message)



        except Exception as e:
            raise e

    # Option 2 Print at the same page

    # Define the CSS class
    st.markdown("""
                <style>
                .paragraph-section {
                    padding: 20px;
                    border-radius: 5px;
                }
                </style>
                """, unsafe_allow_html=True)

    # Display messages and images
    for message in st.session_state.session_history_2:

        # Verify if the message is the same as the current one
        if message['input'] == user_input:
            continue

        st.markdown(f"""
                        <div class="paragraph-section">
                            <b><i>User:</i></b>
                            {message['input']}
                        </div>
                        """, unsafe_allow_html=True)

        if message['img'] is not None:
            st.markdown(f"""
                                        <div class="paragraph-section">
                                            <b><i>Stockbot:</i></b>
                                        </div>
                                        """, unsafe_allow_html=True)
            st.image(message['img'], caption='Stockbot Plot', use_column_width=True)

        if message['content'] is not None:
            text_content = message['content']
            st.markdown(f"""
                            <div class="paragraph-section">
                                <b><i>Stockbot:</i></b>
                                {text_content}
                            </div>
                            """, unsafe_allow_html=True)


elif selected == 'Prediction':
    # Display the content for the Prediction option
    st.title("Prediction")
    st.write("Welcome to the Prediction page.")

elif selected == 'Historic':
    # Option 1 Historic session researches
    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
                <h1>Search History</h1>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 2vh;'>
                <br>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
                <h3>by MDSynergy</h3>
            </div>
            """, unsafe_allow_html=True)

    # Define the CSS class
    st.markdown("""
        <style>
        .paragraph-section {
            padding: 20px;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Display messages and images
    for message in st.session_state.session_history:
        st.markdown(f"""
                <div class="paragraph-section">
                    <b><i>User:</i></b>
                    {message['input']}
                </div>
                """, unsafe_allow_html=True)

        if message['img'] is not None:
            st.markdown(f"""
                                <div class="paragraph-section">
                                    <b><i>Stockbot:</i></b>
                                </div>
                                """, unsafe_allow_html=True)
            st.image(message['img'], caption='Stockbot Plot', use_column_width=True)

        if message['content'] is not None:
            text_content = message['content']
            st.markdown(f"""
                    <div class="paragraph-section">
                        <b><i>Stockbot:</i></b>
                        {text_content}
                    </div>
                    """, unsafe_allow_html=True)

elif selected == 'Alert System':
    st.title("Stock Price Alert System")
    st.write("Welcome to the Stock Alerts page.")
    # Formulario para agregar un nuevo stock
    with st.form('Nuevo Stock'):
        st.header('Ingrese los detalles del stock:')
        company_name = st.text_input('Nombre de la compañía')
        symbol = st.text_input('Símbolo del stock (ejemplo: AAPL para Apple)')

        reference_value = st.number_input('Ingrese el valor de referencia', value=0.0)

        submitted = st.form_submit_button('Añadir')

        if submitted:
            current_stock = get_current_stock_price(symbol)
            if reference_value > current_stock:
                up_down = True
            else:
                up_down = False
            new_stock = {
                'company_name': company_name,
                'symbol': symbol,
                'reference_value': reference_value,
                'up_down': up_down,
                'added': True,
                'last_alert': time.time()
            }
            st.session_state.stocks.append(new_stock)

    # Mostrar datos de seguimiento de stocks
    st.header('Seguimiento de stocks:')
    text_placeholder = st.empty()
    text_placeholder.text("")


    # while True:
    #     if st.session_state.stocks:
    #         for stock in st.session_state.stocks:
    #             if stock.get('added'):
    #                 symbol = stock['symbol']
    #                 company_name = stock['company_name']
    #                 reference_value = stock['reference_value']
    #                 up_down = stock['up_down']
    #                 current_price = get_current_stock_price(symbol)
    #                 alert = check_price_alert(symbol, reference_value, current_price, up_down)
    #                 text = '**{}** ({}): Precio actual: {}'.format(company_name, symbol, current_price)
    #                 text_placeholder.markdown(text)
    #                 # text_placeholder.text('**{}** ({}): Precio actual: {}'.format(company_name, symbol, current_price))
    #                 if alert:
    #                     st.warning(alert)
    #                 time.sleep(2)  # Actualizar cada 5 segundos

    # Initialize a dictionary to store placeholders for each stock
    stock_placeholders = {}

    # Initial setup to create placeholders for each stock
    if st.session_state.stocks:
        for stock in st.session_state.stocks:
            if stock.get('added'):
                symbol = stock['symbol']
                company_name = stock['company_name']
                stock_placeholders[symbol] = st.empty()

    # Continuously update the stock information within their respective placeholders
    while True:
        if st.session_state.stocks:
            for stock in st.session_state.stocks:
                if stock.get('added'):
                    symbol = stock['symbol']
                    company_name = stock['company_name']
                    reference_value = stock['reference_value']
                    up_down = stock['up_down']
                    current_price = get_current_stock_price(symbol)
                    alert = check_price_alert(symbol, reference_value, current_price, up_down)

                    # Update the information in the corresponding placeholder for each stock
                    stock_placeholder = stock_placeholders[symbol]
                    text = f'**{company_name}** ({symbol}): Current Price: {current_price}'
                    stock_placeholder.markdown(text)

                    # Display alerts if triggered and update the alert content
                    if alert:
                        if 'alert' in stock:
                            stock['alert'].empty()  # Clear the previous alert
                        stock['alert'] = st.empty()  # Create a new alert placeholder
                        stock['alert'].warning(alert)

                    time.sleep(2)  # Update every 2 seconds


elif selected == 'Tests':
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
            <h1>Debuggg :p</h1>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 2vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
            <h3>by MDSynergy</h3>
        </div>
        """, unsafe_allow_html=True)

    # Define the CSS class
    st.markdown("""
    <style>
    .paragraph-section {
        padding: 20px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
                <h1>Try 1</h1>
            </div>
            """, unsafe_allow_html=True)

    import streamlit as st
    import yfinance as yf
    import pandas as pd
    import plotly.express as px
    import time

    # Custom CSS to add rounded borders
    css = """
    <style>
    .row-container {
        display: flex;
        flex-direction: row;
        justify-content: space between;
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


    def create_live_stock_chart(ticker):
        fig = px.line(title=f"{ticker} Live Stock Chart")
        return fig


    def fetch_stock_data(ticker):
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1d", interval="5m")
        return stock_data


    def update_live_stock_chart(ticker, stock_data, fig):
        if not stock_data.empty:
            fig.update_xaxes(title_text="Time")
            fig.update_yaxes(title_text="Stock Price")
            fig.update_traces(x=stock_data.index, y=stock_data["Close"], name=ticker)
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

    # Initialize Plotly figures for each ticker
    plotly_figures = {ticker: create_live_stock_chart(ticker) for ticker in ticker_list}

    # Refresh data every 10 seconds (this code block will rerun indefinitely)
    while True:
        time.sleep(10)
        for ticker in ticker_list:
            stock_data = fetch_stock_data(ticker)
            update_live_stock_chart(ticker, stock_data, plotly_figures[ticker])
