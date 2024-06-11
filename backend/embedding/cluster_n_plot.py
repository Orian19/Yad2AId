import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from backend.utils.db_utils import create_connection


def fetch_info():
    """Fetches apartment IDs, city names, and pre-calculated embedding from the SQLite database."""
    con, cur = create_connection()
    cur.execute("""
        SELECT ApartmentId, DescriptionEnglish, Embedding 
        FROM Apartments 
        WHERE DescriptionEnglish IS NOT NULL AND TRIM(DescriptionEnglish) != '' AND Embedding IS NOT NULL
    """)
    result = cur.fetchall()
    ids_embeddings = []
    expected_shape = None

    for row in result:
        apartment_id, description, embedding = row[0], row[1], row[2]
        if embedding is None:
            print(f"Warning: Embedding for Apartment ID {apartment_id} is None")
            continue
        if expected_shape is None:
            expected_shape = embedding.shape
        if embedding.shape == expected_shape:
            ids_embeddings.append((apartment_id, description, embedding))
        else:
            print(f"Warning: Embedding shape {embedding.shape} for Apartment ID {apartment_id} does not match expected {expected_shape}")
    con.close()
    return ids_embeddings

    
data = fetch_info()


# Convert data to DataFrame
df = pd.DataFrame(data, columns=['Apartment_ID', 'Description', 'Embedding'])

# Extract embeddings and convert list of embeddings into a numpy array
X = np.array(df['Embedding'].tolist())

# Dimensionality reduction to 2D using TSNE
tsne = TSNE(n_components=2, random_state=42)
X_reduced = tsne.fit_transform(X)

NUMBER_OF_CLUSTERS = 5

# Perform KMeans clustering on the reduced dimensions
kmeans = KMeans(n_clusters=NUMBER_OF_CLUSTERS, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_reduced)

# Assign cluster labels to the dataframe
df['Cluster'] = clusters

# TF-IDF Vectorization for description analysis
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_tfidf = vectorizer.fit_transform(df['Description'])


exclude_terms = {'sqm', 'apartment', 'room', 'rent', 'nis', 'tel', 'aviv', 'rooms','close','floor'}

# Get top terms for each cluster, excluding specific terms
n_terms = 5
cluster_names = []
for cluster_num in range(NUMBER_OF_CLUSTERS):
    cluster_indices = df['Cluster'] == cluster_num
    cluster_texts = df.loc[cluster_indices, 'Description']
    cluster_tfidf = vectorizer.transform(cluster_texts)
    mean_tfidf = cluster_tfidf.mean(axis=0).A1
    sorted_indices = mean_tfidf.argsort()[::-1]  # Sort indices by TF-IDF value in descending order
    
    top_terms = []
    for index in sorted_indices:
        term = vectorizer.get_feature_names_out()[index]
        if term not in exclude_terms:
            top_terms.append(term)
            if len(top_terms) == n_terms:
                break
    
    cluster_name = ", ".join(top_terms)
    cluster_names.append(cluster_name)

# Plot the apartment IDs on a 2D map
plt.figure(figsize=(20, 12))
colors = [f'C{i}' for i in range(NUMBER_OF_CLUSTERS)]
for cluster_num in range(NUMBER_OF_CLUSTERS):
    cluster_indices = df['Cluster'] == cluster_num
    cluster_points = X_reduced[cluster_indices]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[cluster_num], 
                label=f'Cluster {cluster_num}: {cluster_names[cluster_num]}')
    

    # Draw convex hull around the cluster points
    if len(cluster_points) > 2:
        hull = ConvexHull(cluster_points)
        for simplex in hull.simplices:
            plt.plot(cluster_points[simplex, 0], cluster_points[simplex, 1], colors[cluster_num])

plt.title('Apartment Embeddings in 2D Space with Clustering and Top Terms')
plt.legend(title="Cluster Legends", bbox_to_anchor=(0.75, 1), loc='upper left')
plt.grid(True)
plt.show()