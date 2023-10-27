import numpy as np
from PIL import Image
from streamlit_option_menu import option_menu

from chatgpt import *

selected = "Home"

# Creación del título
st.set_page_config(page_title="MDSynergy")

# if 'messages' not in st.session_state:
#     history = st.session_state['messages']

# 1. as sidebar menu
with st.sidebar:
    # Define a custom style for the option menu to make the background transparent
    custom_style = {"container": {"background-color": "transparent"},
                    "nav-link-selected": {"background-color": "transparent"}, }

    selected = option_menu("Menu", ["Home", 'MD Stockbot', "Prediction", "Historic", "Tests"],
                           icons=['house', 'chat-left-dots-fill', 'bar-chart-line', 'clock', 'bug'], menu_icon="-dots",
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
            st.session_state.session_history.append(current_message)
            st.session_state.session_history_2.insert(0, current_message)

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

        except Exception as e:
            raise e


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
