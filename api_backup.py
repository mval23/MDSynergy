from chatgpt import *

# Streamlit Web Application


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
            else:
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {'role': 'function', 'name': function_name, 'content': function_response})
                second_response = openai.ChatCompletion.create(model='gpt-3.5-turbo-0613',
                                                               messages=st.session_state['messages'])
                st.text(second_response['choices'][0]['message']['content'])
                st.session_state['messages'].append(
                    {'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
        else:
            st.text(response_message['content'])
            st.session_state['messages'].append({'role': 'assistant', 'content': response_message['content']})

    except Exception as e:
        raise e
