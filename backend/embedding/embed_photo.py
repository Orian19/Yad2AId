import json
from PIL import Image
from imgbeddings import imgbeddings
import requests


def embed_photo(url):
    image_to_embed = Image.open(requests.get(url, stream=True).raw)

    ibed = imgbeddings()

    embedded_vector = ibed.to_embeddings(image_to_embed)
    return embedded_vector


def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)  # Load JSON data from file

    if isinstance(data, list):
        for item in data:  # Iterate over each dictionary in the list
            if 'image' in item:  # Check if 'image' key exists in the dictionary
                image_urls = item['image']  # Extract image URLs
                for url in image_urls:
                    try:
                        print(f"Processing {url}")
                        embedding = embed_photo(url)
                        print("First five elements of the embedding vector:", embedding[:5])
                    except Exception as e:
                        print(f"Failed to process {url}: {e}")


# Path to the JSON file
file_path = 'items.json'
process_json_file(file_path)
