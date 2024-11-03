import streamlit as st
import time
from main import my_generator

# Streamlit app structure
st.header('Penerjemah Bahasa Isyarat')

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if message['role'] == 'assistant' and message['video_path'] is not None:
            with open(message['video_path'], "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)

# React to user input
prompt = st.chat_input('Masukkkan kalimat...')
if prompt is not None:
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        {'role': 'user', 'content': prompt})

    progress_text = ''
    my_bar = st.progress(0, text=progress_text)
    path = None
    for value, msg, i in my_generator(prompt):
        progress_text = msg
        path = value
        my_bar.progress(i / 6, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    my_bar = None

    with st.chat_message('assistant'):
        response = 'Tidak dapat menerjemahkan'
        if path is not None:
            response = f'Hasil terjemahan'
            st.markdown(response)
            with open(path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
        else:
            st.markdown(response)

    st.session_state.messages.append(
        {'role': 'assistant', 'content': response, 'video_path': path})
