# AI Jewish book recommendations

## Introduction

The goal of this project is to create a recommendation system for Jewish books. The system will recommend books based on the user's preferences and the books' metadata. The system will be based on a dataset of Jewish books. The dataset will be used to create a vector database of the books. The user will be able to input their preferences and the system will recommend books based on the user's preferences and the books' metadata.

## Dataset

The dataset used in this project is scraped from judaicaplaza.com. They use shopify as their platform. We went to the ["books" collection](https://judaicaplaza.com/collections/books) and appended `/products.json?limit=250&page=1` to the URL to get the first 250 books. We then iterated over the pages to get all the books. Once we had all the books, we saved the data to a JSON and CSV file.

## Data Preprocessing

The most difficult part of building this recommendation system was cleaning the data. Shopify stores descriptions in HTML which needed to be cleaned because of unescaped characters. Another interesting challenge is this store understandable makes very heavy use of product variants. Each variant is broken out into a separate product and takes along some of the parent data along with it. In total, the source data set had 764 products in it and 1365 after breaking out all the variants. There is still some more work that needs to be done to clean up the data, like handling hardcover and softcover books as the same book, but this is a good start.

## Creating the vector database

We are using langchain document loader with embedding created using OpenAI's Text-embedding-ada-002-v2 model. The embedding is created using the book's title, author, and description. The embedding is then used to create a vector database of the books.
