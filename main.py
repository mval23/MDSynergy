import numpy as np
from PIL import Image
from streamlit_option_menu import option_menu

from chatgpt import *

selected = "Home"
history = []

# 1. as sidebar menu
with st.sidebar:
    # Define a custom style for the option menu to make the background transparent
    custom_style = {"container": {"background-color": "transparent"},
                    "nav-link-selected": {"background-color": "transparent"}, }

    selected = option_menu("Menu", ["Home", 'MD Stockbot', "Prediction", "Tests"],
                           icons=['house', 'chat-left-dots-fill', 'bar-chart-line', 'bug'], menu_icon="-dots",
                           default_index=1, styles=custom_style)

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
    st.write("Welcome to the MD Synergy page.")  # todo: add content - David

elif selected == 'MD Stockbot':
    current_message = {'input': None, 'content': None, 'img': None}
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

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

                function_to_call = available_functions[function_name]
                function_response = function_to_call(**args_dict)

                if function_name == 'plot_stock_price':
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
        except Exception as e:
            raise e
    history.append(current_message)
    st.write(history)

elif selected == 'Prediction':
    # Display the content for the Prediction option
    st.title("Prediction")
    st.write("Welcome to the Prediction page.")

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
        background-color: #f0f0f0;  /* You can customize the background color */
    }
    </style>
    """, unsafe_allow_html=True)
    st.write(history)
    # Display messages and images
    for message in history:
        st.markdown(f"""
            <div class="paragraph-section">
                {message['input']}
            </div>
            """, unsafe_allow_html=True)

        if message['img'] is not None:
            st.image(message['img'], caption='Stockbot Plot', use_column_width=True)

        if message['content'] is not None:
            text_content = message['content']
            st.markdown(f"""
                <div class="paragraph-section">
                    {text_content}
                </div>
                """, unsafe_allow_html=True)
