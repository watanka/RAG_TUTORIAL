import streamlit as st
from dotenv import load_dotenv
from langserve import RemoteRunnable
from rag import chain
from langsmith import traceable
load_dotenv()

st.title("Echo Bot")

@traceable
def rag(question):
    stream = st.session_state.rag.invoke(
            {"question": question, 
             "chat_history": [(msg['role'], msg['content']) 
                              for msg in st.session_state.messages
                              if msg['role'] == 'user'
                              ]})
    return stream

# st.session_state.remote_runnable = RemoteRunnable(chain_url)
st.session_state.rag = chain

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('what is up?'):
    with st.chat_message('user'):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({'role': "user", 'content': prompt})


    with st.chat_message('assistant'):
        message_placeholder = st.empty()

        stream = rag(prompt)
        response = st.write(stream)
    st.session_state.messages.append({'role': "assistant", 'content': response})
