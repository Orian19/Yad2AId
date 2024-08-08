import os
import json 

def load_saved_data():
    if os.path.exists('saved_data.json'):
        with open('saved_data.json', 'r') as f:
            return json.load(f)
    return {'description': None, 'description_embedding': None}

def save_saved_data(data):
    with open('saved_data.json', 'w') as f:
        json.dump(data, f)