from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.document_loaders.json_loader import JSONLoader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter

load_dotenv()

splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)


def count_tokens(text):
    return splitter.count_tokens(text=text)


def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["id"] = record.get("id")
    metadata["title"] = record.get("title")
    metadata["tags"] = record.get("tags")
    metadata["image"] = record.get("image")
    metadata["handle"] = record.get("handle")
    metadata["price"] = record.get("price")
    return metadata


def create_vectorstore(documents, embeddings):
    vectorstore = FAISS.from_documents(
        documents=documents, embedding=embeddings)
    summed_tokens = 0
    for product in documents:
        summed_tokens += count_tokens(product.page_content)

    total = summed_tokens / 1000 * 0.0001

    print(f"Total tokens: {summed_tokens}")

    return vectorstore


def save_vectorstore(vectorstore, save_path, index_name):
    vectorstore.save_local(save_path, index_name)
    print("Vectorstore saved to: ", save_path)


loader = JSONLoader(
    file_path='./products.json',
    jq_schema='.[]',
    content_key="expanded_description",
    metadata_func=metadata_func
)

if __name__ == "__main__":
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    vectorstore = create_vectorstore(documents, embeddings)
    save_vectorstore(
        vectorstore, save_path="./book_vectorstore", index_name="products")
