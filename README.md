# AI Jewish book recommendations

## Introduction

The goal of this project is to experiment creating a recommendation system for Jewish books. The system will recommend books based on the user's preferences and the books' metadata. The system will be based on a dataset of Jewish books. The dataset will be used to create a vector database of the books. The user will be able to input their preferences and the system will recommend books based on the user's preferences and the books' metadata.

```
Input:
I am looking for a sefer on chol hamoed. Can you recommend one?

Answer:
Here are some recommendations for a sefer on Chol Hamoed:

1. Title: Chol Hamoed
   Author: Rabbi Moshe Francis, Rabbi Dovid Zucker
   Price: $24.99
   Description: Comprehensive guide to the laws of Chol HaMoed in a clear and practical style.

2. Title: Do You Know Hilchos Chol Hamoed?
   Author: Rabbi Michoel Fletcher
   Price: $14.99
   Description: Family-friendly Halacha sefer focusing on the purpose of Chol Hamoed and experiencing simchas Yom Tov.

3. Title: The Pocket Halacha Series: The Halachos of Chol Hamoed
   Author: Rabbi A. Wiesenfeld
   Price: $5.50
   Description: Practical halachic guidance in a pocket-sized format with commonly asked questions and answers on the laws of Chol Hamoed.
```

## How it works

Given an input, the system will use the vector database to find the most similar books to the input. These books will be injected into the LLM prompt as context and the model will generate a response. The response will be the recommended books.

## How to use

Install the python packages in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

Create an .env file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
<!-- The following are optional. If you would like to use langsmith for observability, create an account at https://smith.langchain.com/ -->
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=your_langsmith_project
```

To use the recommendation service, you need to run the `application/search.py` file.

```bash
python application/search.py
```

The input is hardcoded in the file. Change the input to get different recommendations.

## Development

### Dataset

The dataset used in this project is scraped from judaicaplaza.com. They use shopify as their platform. We went to the ["books" collection](https://judaicaplaza.com/collections/books) and appended `/products.json?limit=250&page=1` to the URL to get the first 250 books. We then iterated over the pages to get all the books. Once we had all the books, we saved the data to a JSON and CSV file.

This dataset is available in the `source_data` folder.

### Data Preprocessing

The most difficult part of building this recommendation system was cleaning the data. Shopify stores descriptions in HTML which needed to be cleaned. Another interesting challenge is this store understandable makes very heavy use of product variants. Each variant is broken out into a separate product and takes along some of the parent data along with it. In total, the source data set had 764 products in it and 1365 after breaking out all the variants. There is still some more work that needs to be done to clean up the data, like handling hardcover and softcover books as the same product, but this is a start.

Run the following files to clean the data.

```bash
python data_preprocessing/init.py
python data_preprocessing/preprocess.py
```

This will create 2 sets of files in the `data_preprocessing` folder.

### Creating the vector database

I are using langchain document loader with embedding created using OpenAI's `Text-embedding-ada-002-v2` model. The embedding is created using the book's title, author, and description. The embedding is then used to create a vector database of the books.

Run the langchain document loader to create the vector database.

```bash
python data_preprocessing/langchain_doc_loader.py
```

This will create `products.faiss` and `products.pkl` files in the `book_vectorstore` folder.

## Future work

I would like to flesh this out more. Here are some ideas in no specific order:

- Setup a web interface for the recommendation system.
- Expand the chain to chat with the user to get more information about their preferences.
- Use the user's preferences to create a user profile and use it to recommend books.
- Allow the user to rate the recommended books and use the ratings to improve the recommendations.
- Allow the user to continue the conversation with the system to get more recommendations or ask questions about the books.
- Cleanup the preprocessing code and make it more robust. Merge the init.py and preprocess.py files and process all of the data in pandas.
- Built out more robust handling of the product variants and options.
- Experiment with different models and embeddings to see if we can get better recommendations.
- Experiment using different retrieval methods to get the most similar books.
- Better handle searches for seforim in Hebrew.
- Add voice input and output to the system.
- Create a Jupyter notebook for this repo.
