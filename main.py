import json
from datetime import time
import numpy as np
import openai
from streamlit_option_menu import option_menu

from chatgpt import *

selected = "Home"

# Creación del título
st.set_page_config(page_title="MDSynergy")

# Inicialización de stocks en la sesión si no existe
if 'stocks' not in st.session_state:
    st.session_state.stocks = []

# Logo de la empresa (reemplaza 'path/to/logo.png' con la ruta real de tu logo)
logo_path = 'MD.png'  # 'path/to/logo
logo_size = (100, 100)  # Ajusta el tamaño del logo según sea necesario

# Aplicar transparencia a los bordes del logo
logo_with_transparency = apply_transparency(logo_path, border_size=10)

# Logo en la barra lateral
st.sidebar.image(logo_with_transparency, use_column_width=True)

# 1. as sidebar menu
with st.sidebar:
    # Define a custom style for the option menu to make the background transparent
    custom_style = {"container": {"background-color": "transparent"},
                    "nav-link-selected": {"background-color": "transparent"}, }

    selected = option_menu("Menu", ["Home", 'MD Stockbot', "History", "Stock Alerts"],
                           icons=['house', 'chat-left-dots-fill', 'clock', 'exclamation-triangle-fill'],
                           menu_icon="-dots", default_index=0, styles=custom_style)


if selected == 'Home':
    # Display the content for MD Synergy
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
            <h1>🚀 MD Synergy 🌐</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 2vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
            <h3>by MDSynergy </h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)

    # Descripción de la empresa
    st.markdown("""
        <div style='display: flex; align-items: center; height: 5vh;'>
            <h4>Welcome to MDSynergy! 🌟</h4>
        </div>
        """, unsafe_allow_html=True)
    st.write(
        "We are dedicated to providing innovative solutions in the field of data analysis and financial technology. 💡")

    # Sección de información de proyectos
    st.write("## Projects 🚧")

    # Proyecto 1: Stock Analysis Chatbot Assistant
    st.write("### 1. Stock Analysis Chatbot Assistant 📈🤖")

    # Descripción del proyecto
    st.write(
        "The Stock Analysis Chatbot Assistant is our latest project. It's a chatbot designed to help users analyze stock market data and perform financial analyses. The chatbot leverages OpenAI's GPT-3.5 Turbo model for an intuitive and efficient user experience. 🚀")

    # Variable de sesión para rastrear el estado del botón
    button_state = st.session_state.get("button_state", False)

    # Botón para mostrar/ocultar información del proyecto
    if st.button("Learn More ℹ️"):
        button_state = not button_state  # Invertir el estado del botón

    # Sección de información del proyecto si el botón está activado
    if button_state:
        # Título de la sección de Características Clave
        st.write("# Stock Analysis Chatbot Assistant")

        st.write(
            "Welcome to the Stock Analysis Chatbot Assistant project by Mariana and David! Our chatbot provides an easy-to-use interface for accessing real-time stock market data and performing financial analyses. Read on to learn more about our project, how to run the application, and its key features. 🌐💬")

        st.write(
            "The Stock Analysis Chatbot Assistant is your personal financial sidekick. It's designed to help you with stock market data, financial metrics, and visualizing stock price trends. We've harnessed the capabilities of OpenAI's GPT-3.5 Turbo model to make this experience intuitive and efficient. 🤖📊")

        # Título de la sección de Características Clave
        st.write("## Key Features 🌟")

        # Lista de características clave con viñetas
        st.write("- **Chat with Ease**: Interact with our chatbot using a simple and friendly chat-based interface. 💬")
        st.write(
            "- **Up-to-the-Minute Data**: Get the latest stock prices by simply providing the company's name or stock symbol. 📈")
        st.write(
            "- **Financial Insights**: Access common financial metrics, including Simple Moving Average (SMA), Exponential Moving Average (EMA), Moving Average Convergence Divergence (MACD), and Relative Strength Index (RSI). 💹")
        st.write(
            "- **Visualize Data**: Love charts? Our chatbot can generate and display stock price charts at your request. 📊")

        # Posible sección con enlaces adicionales
        st.write("## Additional Resources 📚")
        st.write(
            "- [Documentation 📖](https://docs.google.com/document/d/1yp1PhlK84x1-NgHQegXYdC8W2aNeRoKlFivmw2typ6c/edit)")
        st.write("- [Project Repository 🛠️](https://github.com/mval23/MDSynergy)")
        st.write("- Contact us at [mdsynergy73@gmail.com] 📧")

        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
                <br>
            </div>
            """, unsafe_allow_html=True)

        # Posible sección de pie de página
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
                <h4>Enjoy analyzing stocks with 📈</h4>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
                <h4>MDSynergy's Stock Analysis Chatbot Assistant! 🤖💼</h4>
            </div>
            """, unsafe_allow_html=True)
        st.image("MDD.png", caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
        st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
                <br>
            </div>
            """, unsafe_allow_html=True)


    # Guardar el estado del botón en la sesión
    st.session_state.button_state = button_state

    # Sección "About Us"
    st.write("## About Us 💻👫")

    # Breve historia de MDSynergy
    st.write(
        "MDSynergy was founded by two passionate Computer Science students, Mariana and David. Their shared vision and commitment to excellence led them to create a company that reflects their combined expertise and aspirations. 🚀")

    st.write(
        "The name 'MDSynergy' is derived from the initials of our founders. It represents the synergy created by bringing together their unique skills and perspectives. 🌐")

    st.write(
        "Mariana and David started MDSynergy with the purpose of generating and applying the knowledge they gained throughout their studies. Their relentless dedication, recognition, and ambition propelled them forward, and they continued to develop innovative solutions in the field of data analysis and financial technology. 💡")

    # Llamada a la acción
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
            <h4>Explore our projects to discover how MDSynergy is 🚀</h4>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; height: 5vh;'>
                <h4>revolutionizing data analysis and technology. 🌐💻</h4>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 10vh;'>
            <br>
        </div>
        """, unsafe_allow_html=True)


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

    st.write("\n")
    st.write("\n")
    st.write("Hey there, Rockstar Investor! 🌟 Welcome to 'MD Stockbot 🤖💼,' your trusty Stock Analysis Chatbot Assistant!")

    st.write("\n**How to Roll:**")
    st.write("1. Just drop your stock questions or magic words in the 'Your input:' zone.")
    st.write("2. Watch Stockbot do its thing – real-time stock prices, insights, and even some snazzy visuals!")
    st.write("3. Rewind time and revisit your past stock chats in the chat history.")

    st.write("\n**Why it's Awesome:**")
    st.write("- Effortlessly snag the latest stock prices.")
    st.write("- Crunch numbers with cool indicators like SMA, EMA, RSI, and MACD.")
    st.write("- Check out flashy stock plots for some serious visual vibes.")
    st.write("- Banter with our laid-back Stockbot in this epic stock adventure.")

    st.write("\n**Ready to Rock the Stock World? Let's Chat! 🚀📈**")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
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
                    args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window'),
                                 'num_std_dev': function_args.get('num_std_dev')}

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


elif selected == 'History':
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

    st.write("\n")
    st.write("\n")

    st.write("Explore Your Stockbot Conversations! 🕰️")
    st.write(
        "Dive into your journey with Stockbot through the 'History' page. Here, you can rewind and relive past interactions. The page showcases your questions, Stockbot's responses, and any intriguing visuals it shared.")

    st.write("\n**What to Expect:**")
    st.write("- A detailed timeline of your conversations with Stockbot.")
    st.write("- User inputs and Stockbot replies presented in an easy-to-follow format.")
    st.write("- Catch a glimpse of any charts or images shared during your past sessions.")

    st.write("\n**Stay Connected with Your Stockbot Journey! 📊✨**")

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")

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

elif selected == 'Stock Alerts':
    st.markdown("""
                <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
                    <h1>Stock Price Alert System</h1>
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

    st.write("\n")
    st.write("\n")

    st.write("Welcome to Stock Alerts! 🚀 \nTrack your favorite stocks effortlessly and get alerts when they hit your target prices. 📈")
    st.write("\n**How it works:**")
    st.write("1. Add a stock with its name, symbol, and your alert price.")
    st.write("2. Watch real-time updates and get notified when it's time to act.")
    st.write("\nStay informed, invest smartly! 📈✨")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    # Formulario para agregar un nuevo stock
    with st.form('New Stock'):
        st.header('Enter Stock Details:')
        company_name = st.text_input('Company Name')
        symbol = st.text_input('Stock Symbol (example: AAPL for Apple)')

        reference_value = st.number_input('Enter Reference Value', value=0.0)

        submitted = st.form_submit_button('Add')

        if submitted:
            current_stock = get_current_stock_price(symbol)
            if reference_value > current_stock:
                up_down = True
            else:
                up_down = False
            new_stock = {'company_name': company_name, 'symbol': symbol, 'reference_value': reference_value,
                'up_down': up_down, 'added': True, 'last_alert': time.time()}
            st.session_state.stocks.append(new_stock)

    # Mostrar datos de seguimiento de stocks
    st.header('Stock Tracking:')
    text_placeholder = st.empty()
    text_placeholder.text("")


    # Initialize a dictionary to store placeholders for each stock
    stock_placeholders = {}

    # Initial setup to create placeholders for each stock
    if st.session_state.stocks:
        for stock in st.session_state.stocks:
            if stock.get('added'):
                symbol = stock['symbol']
                company_name = stock['company_name']
                stock_placeholders[symbol] = {'info_placeholder': st.empty(), 'fig': None, 'data_fetched': False}

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
                    stock_placeholder['info_placeholder'].markdown(
                        f'**{company_name}** ({symbol}): Current Price: {current_price}')

                    # Fetch stock data only once
                    if not stock_placeholder['data_fetched']:
                        stock_data = fetch_stock_data(symbol)
                        stock_placeholder['fig'] = create_live_stock_chart(symbol, stock_data)
                        stock_placeholder['data_fetched'] = True

                    if stock_placeholder['fig'] is not None:
                        # Update the live stock chart with new data
                        stock_data = fetch_stock_data(symbol)
                        update_live_stock_chart(symbol, stock_data, stock_placeholder['fig'])

                    # Display alerts if triggered and update the alert content
                    if alert:
                        if 'alert' in stock:
                            stock['alert'].empty()  # Clear the previous alert
                        stock['alert'] = st.empty()  # Create a new alert placeholder
                        stock['alert'].warning(alert)

                    time.sleep(2)  # Update every 2 seconds
