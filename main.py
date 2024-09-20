from langchain_openai import OpenAIEmbeddings
from repository import ChromaRepository

from langchain_core.documents import Document
from crawl import TrafilaturaCrawler
from langchain_chroma import Chroma
from data_handle import ChromaDataHandler
from update_db import ChromaDailyUpdater
from dotenv import load_dotenv


load_dotenv()

crawler = TrafilaturaCrawler()
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="real_estate",
    embedding_function = embeddings,
    persist_directory="./real_estate"
)

repo = ChromaRepository(vector_store)


data_handler = ChromaDataHandler()
updater = ChromaDailyUpdater(repo)

feed_url = "https://www.mk.co.kr/rss/50300009/"



parse_contents = crawler.crawl(feed_url)
# preprocessed_contents = 
parse_contents = [Document(content) for content in parse_contents]

updater.update(parse_contents) 
