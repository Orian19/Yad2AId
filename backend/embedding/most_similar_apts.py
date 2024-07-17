import random
import numpy as np
from backend.utils.db_utils import create_connection
from sklearn.metrics.pairwise import cosine_similarity

def fetch_liked_apts():
    """Fetches apartment IDs and pre-calculated embedding from the liked apartments SQLite database."""
    con, cur = create_connection()
    cur.execute("""
        SELECT ApartmentId, Embedding 
        FROM UserLikedApartments  
        WHERE Embedding IS NOT NULL
    """)
    result = cur.fetchall()
    ids_embeddings = []
    expected_shape = None

    for row in result:
        apartment_id, embedding = row[0], row[1]
        if embedding is None:
            print(f"Warning: Embedding for Apartment ID {apartment_id} is None")
            continue
        if expected_shape is None:
            expected_shape = embedding.shape
        if embedding.shape == expected_shape:
            ids_embeddings.append((apartment_id, embedding))
        else:
            print(f"Warning: Embedding shape {embedding.shape} for Apartment ID {apartment_id} does not match expected {expected_shape}")
    con.close()
    return ids_embeddings


def fetch_target_apt(target_ids: list, liked_apts: list):
    """Fetches apartment IDs and pre-calculated embedding from the potential apartments SQLite database 
    for given list of target IDs, excluding those already liked."""
    con, cur = create_connection()
    
    # Extract apartment IDs from liked_apts
    liked_ids = {apt[0] for apt in liked_apts}  
    
    # Filter target_ids to remove any that are in liked_apts
    filtered_target_ids = [id for id in target_ids if id not in liked_ids]
    
    # Convert the filtered list of IDs to a format that can be used in a SQL query
    ids_tuple = tuple(filtered_target_ids)
    
    # Execute the SQL query only if the filtered_target_ids list is not empty
    if ids_tuple:
        query = f"""
            SELECT ApartmentId, Embedding 
            FROM Apartments
            WHERE ApartmentId IN {ids_tuple} AND Embedding IS NOT NULL
        """
        cur.execute(query)
        result = cur.fetchall()
    else:
        result = []

    ids_embeddings = [(row[0], row[1]) for row in result]
    con.close()
    return ids_embeddings

def most_similar_apts(target_ids: list):
    """
    Finds the most similar apartment from a list of target apartment IDs based on the centroid of liked apartment embeddings.
    """
    try:
        liked_ids_embeddings = fetch_liked_apts()
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
        target_embeddings = fetch_target_apt(target_ids,liked_ids_embeddings)
        if not target_embeddings:
            return None, "No target apartments available."

        # Calculate similarity of each target embedding to the centroid
        target_data = np.array([embedding for _, embedding in target_embeddings])
        similarities = cosine_similarity(target_data, centroid).flatten()

        # Find the index of the maximum similarity
        max_index = np.argmax(similarities)
        most_similar_id = target_embeddings[max_index][0]
    
        return most_similar_id, "Apartment found successfully."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"
