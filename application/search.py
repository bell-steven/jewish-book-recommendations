from utils import load_vectorstore
import os
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


vectorstore = load_vectorstore(
    vectorstore_path="./book_vectorstore", index_name="products")

retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k": 6})

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
prompt = hub.pull("rlm/rag-prompt")
example_messages = prompt.invoke(
    {"context": "filler context", "question": "filler question"}
).to_messages()
example_messages

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

for chunk in rag_chain.stream("Reb Moshe on Pesach"):
    print(chunk, end="", flush=True)
