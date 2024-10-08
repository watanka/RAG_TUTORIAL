from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from datetime import datetime

load_dotenv()

llm = ChatOpenAI(temperature=0)

# Map
map_template = """The following is a set of documents
{docs}
You are an expertised realtor. Based on numbers and facts, you need to analyze how real estate trends are. Area, dates, and numbers are very important factors to analyze.
Give me an Analysis stated with the facts and numbers.
Helpful Answer:"""
map_prompt = PromptTemplate.from_template(map_template)
map_chain = LLMChain(llm=llm, prompt=map_prompt)


# Reduce
reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the main themes. Answer should be in Korean.
Helpful Answer:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)

# Run chain
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# Takes a list of documents, combines them into a single string, and passes this to an LLMChain
combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="docs"
)

# Combines and iteratively reduces the mapped documents
reduce_documents_chain = ReduceDocumentsChain(
    # This is final chain that is called.
    combine_documents_chain=combine_documents_chain,
    # If documents exceed context for `StuffDocumentsChain`
    collapse_documents_chain=combine_documents_chain,
    # The maximum number of tokens to group documents into.
    token_max=4000,
)

# Combining documents by mapping a chain over them, then combining results
map_reduce_chain = MapReduceDocumentsChain(
    # Map chain
    llm_chain=map_chain,
    # Reduce chain
    reduce_documents_chain=reduce_documents_chain,
    # The variable name in the llm_chain to put the documents in
    document_variable_name="docs",
    # Return the results of the map steps in the output
    return_intermediate_steps=False,
)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0
)




def summarize(doc_str):
    # 현재 날짜와 시간 가져오기
    now = datetime.now()
    # 원하는 포맷으로 변환
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    docs = Document(page_content=doc_str,
                    metadata = {'collect_date': formatted_date_time}
                    )
    split_docs = text_splitter.split_documents([docs])
    summary = map_reduce_chain.invoke(split_docs)
    return summary


def write_newsletter(db, date: str):
    '''
    db에서 조건(날짜, 지역 등)에 속하는 정보들을 쿼리해옴.
    '''
    pass

