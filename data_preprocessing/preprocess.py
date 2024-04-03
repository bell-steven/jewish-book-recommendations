from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import time
import json
import pandas as pd
pd.set_option("display.max_colwidth", 1000)
load_dotenv()

file_path = './cleaned_judaica_books.json'

with open(file_path, 'r') as file:
    all_products = json.load(file)


def create_expanded_description(row):

    if row["body_html"] == "" and row["tags"] == "":
        row["expanded_description"] = row["title"]
    elif row["body_html"] == "" and row["tags"] != "":
        row["expanded_description"] = "Title: " + \
            row['title'] + " Tags: " + row['tags']
    elif row["body_html"] != "" and row["tags"] == "":
        row["expanded_description"] = "Title: " + \
            row['title'] + " Description: " + row["body_html"]
    else:
        row["expanded_description"] = "Title: " + row['title'] + \
            " Description: " + row["body_html"] + " Tags: " + str(row['tags']) + \
            " Vendor: " + row['vendor'] + " Price: " + row['price'] + " Options: " + \
            str(row['options'])
    return row


def df_preprocessing(df):
    df.fillna("", inplace=True)
    df = df.apply(lambda row: create_expanded_description(row), axis=1)
    df = df.rename(columns={"body_html": "description"})
    df = df[["id", "title", "handle", "description",
             "expanded_description", "tags", "image", "price"]]
    return df


product_df = pd.DataFrame(all_products)
cleaned_df = df_preprocessing(product_df)


cleaned_df.to_csv("products.csv", index=False)
cleaned_products_json = cleaned_df.to_json(orient="records")
with open("products.json", "w") as f:
    f.write(cleaned_products_json)
