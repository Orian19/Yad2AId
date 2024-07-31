import random
import numpy as np
from utils.db_utils import create_connection
from embedding.create_embedding import get_embedding
from sklearn.metrics.pairwise import cosine_similarity


def get_embedding_for_apartment(apt_id):
    """
    Retrieve the embedding for a given apartment ID from the Apartments table.
    """
    con, cur = create_connection()
    try:
        cur.execute("""
            SELECT Embedding
            FROM Apartments 
            WHERE ApartmentId = ?
        """, (apt_id,))
        result = cur.fetchone()
        if result:
            embedding = result[0]
            return embedding
        else:
            print(f"Warning: No embedding found for Apartment ID {apt_id}")
            return None
    except Exception as e:
        print(f"Error fetching embedding for Apartment ID {apt_id}: {e}")
        return None
    finally:
        con.close()


def fetch_liked_apts(user_id):
    """Fetches apartment IDs and pre-calculated embedding from the liked apartments SQLite database."""
    con, cur = create_connection()
    cur.execute("""
        SELECT ApartmentId
        FROM UserLikedApartments  
        WHERE UserId = ?
    """, (user_id,))
    result = cur.fetchall()
    ids_embeddings = []
    expected_shape = None

    for row in result:
        apartment_id = row[0]
        embedding = get_embedding_for_apartment(apartment_id)
        if embedding is None:
            print(f"Warning: Embedding for Apartment ID {apartment_id} is None")
            continue
        if expected_shape is None:
            expected_shape = embedding.shape
        if embedding.shape == expected_shape:
            ids_embeddings.append((apartment_id, embedding))
        else:
            print(
                f"Warning: Embedding shape {embedding.shape} for Apartment ID {apartment_id} does not match expected {expected_shape}")
    con.close()
    return ids_embeddings


def fetch_target_apt(target_ids: list, liked_apts: list):
    con, cur = create_connection()

    liked_ids = {apt[0] for apt in liked_apts}
    filtered_target_ids = [id for id in target_ids if id not in liked_ids]

    if filtered_target_ids:
        # Use placeholders in the query and pass the list directly to execute
        placeholders = ','.join('?' * len(filtered_target_ids))
        query = f"""
            SELECT ApartmentId, Embedding 
            FROM Apartments
            WHERE ApartmentId IN ({placeholders}) AND Embedding IS NOT NULL
        """
        cur.execute(query, filtered_target_ids)
        result = cur.fetchall()
    else:
        result = []

    ids_embeddings = [(row[0], row[1]) for row in result]
    con.close()
    return ids_embeddings


def most_similar_apts(target_ids: list, user_id: int, description=None):
    """
    Finds the most similar apartment from a list of target apartment IDs based on the centroid of liked apartment embeddings.
    """
    try:
        # Handle edge case of only one apartment left with similar "dry" details
        if len(target_ids) == 1:
            return target_ids[0]

        liked_ids_embeddings = fetch_liked_apts(user_id)
        # If user inserted a description take it into account
        if description != None:
            liked_ids_embeddings.insert(0, (0, get_embedding(description)))

        if not liked_ids_embeddings:
            # Return a random apartment ID from the target_ids list
            if not target_ids:
                return None, "No target apartments available."
            random_id = random.choice(target_ids)
            return random_id, "Random apartment ID returned due to no liked apartments available."

        # Compute the centroid of the liked apartment embeddings
        embeddings = np.array([embedding for _, embedding in liked_ids_embeddings])
        centroid = np.mean(embeddings, axis=0).reshape(1, -1)

        # Fetch embeddings of target apartments
        target_embeddings = fetch_target_apt(target_ids, liked_ids_embeddings)
        if not target_embeddings:
            return None, "No target apartments available."

        # Calculate similarity of each target embedding to the centroid
        target_data = np.array([embedding for _, embedding in target_embeddings])
        similarities = cosine_similarity(target_data, centroid).flatten()

        # Find the index of the maximum similarity
        max_index = np.argmax(similarities)
        most_similar_id = target_embeddings[max_index][0]

        return most_similar_id
    except Exception as e:
        return None, f"An error occurred: {str(e)}"
