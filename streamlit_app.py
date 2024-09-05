import streamlit as st
import chromadb
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain import hub
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

st.title("Echo Bot")

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


embedding = OpenAIEmbeddings()
persist_directory = 'db'
persistent_client = chromadb.PersistentClient()


vectordb = Chroma(
    client = persistent_client,
    persist_directory=persist_directory,
    embedding_function=embedding
)

retriever = vectordb.as_retriever(search_kwargs = {'k': 3})
prompt = hub.pull('rlm/rag-prompt') ## prompt 종류

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)






# Initialize chat history
if 'messages' not in st.session_state:
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
    st.session_state.messages.append({'role': 'user', 'content': prompt})


    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        for response in rag_chain.invoke(
            input = [
                {'role': m['role'], 'content': m['content']}
                for m in st.session_state.messages
            ]
        ):
            full_response += response.choices[0].delta.get('content', '')
            message_placeholder.markdown(full_response + ' ')
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({'role': 'assitant', 'content': response})
