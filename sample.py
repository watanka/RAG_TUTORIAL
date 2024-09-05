import os
import chromadb
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("post-content", "post-title", "post-header")
#         )
#     ),
# )
# docs = loader.load()

embedding = OpenAIEmbeddings()
persist_directory = 'db'
persistent_client = chromadb.PersistentClient()


query = "내 이름이 뭔지 알아? 지금 뭐하고 있게?"
vectordb = Chroma.from_texts([
    "2024년 09월 04일, 나는 지금 스파르타 AI 필진을 위한 글을 작성중에 있어. 내 이름은 신은성이야.",
],
        client=persistent_client,
        embedding=embedding,
        persist_directory=persist_directory
)



vectordb = None



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

print(rag_chain.invoke(query))

