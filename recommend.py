from typing import List
from embed import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommendations_from_strings(database: List[str], index_of_source_string: int, model="text-embedding-ada-002") -> List[int]:
    """Return nearest neighbors of a given string based on cosine similarity of embeddings."""

    # Get embeddings for all strings
    embeddings = [get_embedding(s, model=model) for s in database]
    embeddings_matrix = np.array(embeddings)

    # Calculate cosine similarities with the source string embedding
    similarities = cosine_similarity(embeddings_matrix, embeddings_matrix[index_of_source_string:index_of_source_string+1])

    # Sort the indices of embeddings based on similarity in descending order (higher is more similar)
    nearest_neighbors = np.argsort(-similarities.ravel())

    # Exclude the source index and return the result
    return list(nearest_neighbors[nearest_neighbors != index_of_source_string])

