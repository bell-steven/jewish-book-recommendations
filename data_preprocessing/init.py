import json
import csv
from bs4 import BeautifulSoup

# Simulated data loading from a file
# Placeholder file path variable
file_path = '../source_data/judaica_books.json'

with open(file_path, 'r') as file:
    data = json.load(file)

# clean html
for item in data:
    soup = BeautifulSoup(item['body_html'], 'html.parser')
    item['body_html'] = soup.get_text()

# go through each item and remove the 'handle', 'created_at', 'product_type', 'product_type' keys.
for item in data:
    item.pop('created_at', None)
    item.pop('product_type', None)
    item.pop('published_at', None)

# remove "Books", "giftwrap", "GM" from the 'tags' list of each item.
for item in data:
    item['tags'] = [tag for tag in item['tags']
                    if tag not in ["Books", "giftwrap", "GM"]]

all_products = []


def get_image(featured_image, images):
    if featured_image:
        return featured_image['src']
    elif images:
        return images[0]['src']
    else:
        return ''


for item in data:
    for variant in item['variants']:
        new_item = {}
        new_item['id'] = variant['id']
        new_item['parent_id'] = variant['product_id']
        new_item['handle'] = item['handle']
        new_item['vendor'] = item['vendor']
        new_item['tags'] = item['tags']
        new_item['options'] = item['options']
        new_item['title'] = item['title'] if variant['title'] == 'Default Title' else variant['title']
        new_item['body_html'] = item['body_html']
        new_item['option1'] = variant['option1']
        new_item['option2'] = variant['option2']
        new_item['option3'] = variant['option3']
        new_item['sku'] = variant['sku']
        new_item['requires_shipping'] = variant['requires_shipping']
        new_item['taxable'] = variant['taxable']
        new_item['image'] = get_image(
            variant['featured_image'], item['images'])
        new_item['available'] = variant['available']
        new_item['price'] = variant['price']
        new_item['grams'] = variant['grams']
        new_item['compare_at_price'] = variant['compare_at_price']
        new_item['position'] = variant['position']
        all_products.append(new_item)

# Save the cleaned data to a JSON file
cleaned_file_path = './cleaned_judaica_books.json'
with open(cleaned_file_path, 'w') as file:
    json.dump(all_products, file)

# Save the cleaned data to a CSV file
cleaned_csv_file_path = './cleaned_judaica_books.csv'
with open(cleaned_csv_file_path, 'w') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(all_products[0].keys())
    for item in all_products:
        csv_writer.writerow(item.values())

# sample file with only 3 items
sample_file_path = './sample_judaica_books.json'
with open(sample_file_path, 'w') as file:
    json.dump(all_products[:3], file)
