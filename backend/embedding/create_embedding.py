import openai
from dotenv import load_dotenv
import numpy as np
import os

# load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def normalize_l2(x):
    """Normalize an array to L2 norm."""
    if np.linalg.norm(x) == 0:
        return x
    return x / np.linalg.norm(x)


def get_embedding(text, model="text-embedding-ada-002"):
    """Fetch and normalize the embedding for a given text."""
    response = openai.Embedding.create(input=text, model=model)
    embedding = response['data'][0]['embedding']
    return normalize_l2(embedding)
