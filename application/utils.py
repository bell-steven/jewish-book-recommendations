from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()


def load_vectorstore(vectorstore_path, index_name):
    vectorstore = FAISS.load_local(
        folder_path=vectorstore_path, index_name=index_name, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    return vectorstore
