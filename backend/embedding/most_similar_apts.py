import numpy as np

from embedding.cities_n_plot import fetch_ids_and_embeddings


def find_nearest_neighbors(liked_ids_embeddings=fetch_ids_and_embeddings()):
    """
    Find the nearest neighbor for each apartment's pre-fetched embedding.
    :param liked_ids_embeddings: List of tuples containing apartment ID, city name, and embedding
    :return: Dictionary of apartment ID to nearest neighbor's apartment ID
    """
    apartment_id, city_name, embedding = zip(*liked_ids_embeddings)
    embeddings = np.array(embedding)

    # Compute cosine similarity matrix (since embeddings are normalized, this can be done using dot product)
    similarity_matrix = np.dot(embeddings, embeddings.T)
    np.fill_diagonal(similarity_matrix, -np.inf)  # to ignore self-similarity

    # Find the index of the maximum similarity for each embedding (excluding self)
    nearest_indices = np.argmax(similarity_matrix, axis=1)
    nearest_ids = [apartment_id[idx] for idx in nearest_indices]

    return dict(zip(apartment_id, nearest_ids))


# example
# ids_embeddings = fetch_ids_and_embeddings()
# nearest_neighbors = find_nearest_neighbors(ids_embeddings)
