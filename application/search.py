from utils import load_vectorstore
import os
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


vectorstore = load_vectorstore(
    vectorstore_path="./book_vectorstore", index_name="products")

retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k": 6})

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

template = """You are a chatbot for a jewish bookstore. Your job is to make book and seforim recommendations bases on available data such as season, upcoming holiday or yom tov, or topic specified by the user in the question. Based on the available data, recommend books that align with these interests. Provide a brief summarized description of each recommendation, including its relevance to the user's interests.

If possible, include books from different genres and ask for user feedback in narrowing down the search. Keep the output concise and only include relevant information such as the title, author price and a very brief summarized description. You can also show a single sentence with reasoning of why a choice is relevant. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}

Question: {question}

Helpful Answer:
"""
custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

for chunk in rag_chain.stream("I am looking for a new haggadah for yom tov. Can you recommend one?"):
    print(chunk, end="", flush=True)
