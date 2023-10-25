from chatgpt import *
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Streamlit Web Application

# Create a menu bar in the sidebar
st.sidebar.title("Menu")

# Define menu options
menu_options = ["MD Synergy", "MD Stockbot", "Prediction", "Tests"]

# Create button-like options in the sidebar
selected_option = st.sidebar.radio("Select an option", menu_options)

list_messages = []

if selected_option == "MD Synergy":
    # Display the content for MD Synergy
    st.title("MD Synergy")
    st.write("Welcome to the MD Synergy page.")
elif selected_option == "MD Stockbot":
    # Display the content for MD Stockbot
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 8vh;'>
            <h1>MD Stockbot</h1>
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

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    user_input = st.text_input('Your input:')

    current_message = {'input': user_input, 'content': None, 'img': None}

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
                    plt.imshow(image_array, cmap='gray')
                    plt.savefig('stock.png')  # Save the image as 'stock.png'
                    st.session_state['messages'].append({'role': 'img', 'content': 'stock.png'})
                    image = Image.open('stock.png')  # Replace 'your_image.png' with your image file path
                    image_array = np.array(image)
                    current_message['content'] = image_array
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
                    current_message['content'] = message
                    st.session_state['messages'].append({'role': 'assistant', 'content': message})
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
                st.session_state['messages'].append({'role': 'assistant', 'content': message})
            list_messages.append(current_message)
        except Exception as e:
            raise e

elif selected_option == "Prediction":
    # Display the content for the Prediction option
    st.title("Prediction")
    st.write("Contact us here.")

elif selected_option == "Tests":
    # Display the content for the Prediction option
    st.title("Prediction")
    st.write("Contact us here.")

    # Custom CSS for the paragraph section
    st.markdown("""
        <style>
        .paragraph-section {
            padding: 20px;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True, )

    # Define the text content using a variable
    text_content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, \
     dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, \
     varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non \
     fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."

    # Create a section with flexible height but a fixed width
    st.markdown(f"""
        <div class="paragraph-section">
            {text_content}
        </div>
        """, unsafe_allow_html=True, )

    st.title("Conversation History")
    # if 'messages' in st.session_state:
    #     for message in st.session_state['messages']:
    #         if message['role'] == 'user':
    #             st.markdown(f"**Input:** {message['content']}")
    #         elif message['role'] == 'assistant':
    #             st.markdown(f"**Assistant:** {message['content']}")
    #         elif message['role'] == 'img':
    #             st.image(message['content'], caption='Loaded Image', use_column_width=True)

    for m in list_messages:
        st.markdown(f"**User:** {m['input']}")
        if m['content'] != None:
            st.markdown(f"**Stockbot:** {m['content']}")
        if m['img'] != None:
            # Display the image in Streamlit
            st.image(m['img'], caption='Stockbot Plot', use_column_width=True)

