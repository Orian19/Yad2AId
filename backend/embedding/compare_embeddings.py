from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

from embedding.embed import create_connection


def fetch_ids_and_embeddings():
    """Fetches apartment IDs and pre-calculated embedding from the SQLite database."""
    con, cur = create_connection()
    cur.execute("SELECT ApartmentId, Embedding FROM Apartments WHERE Description IS NOT NULL AND TRIM(Description) != '' AND Embedding IS NULL")
  # Adjust table and column names if necessary
    result = cur.fetchall()
    ids_embeddings = []
    expected_shape = None  # We will determine this from the first valid embedding.

    for row in result:
        embedding = row[1]
        if embedding is None:
            print(f"Warning: Embedding for Apartment ID {row[0]} is None")
            continue
        if expected_shape is None:
            expected_shape = embedding.shape  # Set expected shape based on the first embedding
        if embedding.shape == expected_shape:
            ids_embeddings.append((row[0], embedding))
        else:
            print(
                f"Warning: Embedding shape {embedding.shape} for Apartment ID {row[0]} does not match expected {expected_shape}")
    con.close()
    return ids_embeddings


def plot_embeddings(ids_embeddings):
    """Plots pre-fetched embeddings with interactive tooltips showing IDs."""
    ids, embeddings = zip(*ids_embeddings)
    embeddings = np.array(embeddings)

    tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
    embeddings_2d = tsne.fit_transform(embeddings)

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])

    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f"Apartment ID: {ids[ind['ind'][0]]}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.title('Apartment Embeddings')
    plt.show()


def find_nearest_neighbors(ids_embeddings):
    """Find the nearest neighbor for each apartment's pre-fetched embedding."""
    ids, embeddings = zip(*ids_embeddings)
    embeddings = np.array(embeddings)

    # Compute cosine similarity matrix (since embeddings are normalized, this can be done using dot product)
    similarity_matrix = np.dot(embeddings, embeddings.T)
    np.fill_diagonal(similarity_matrix, -np.inf)  # to ignore self-similarity

    # Find the index of the maximum similarity for each embedding (excluding self)
    nearest_indices = np.argmax(similarity_matrix, axis=1)
    nearest_ids = [ids[idx] for idx in nearest_indices]

    return dict(zip(ids, nearest_ids))


# Example usage
ids_embeddings = fetch_ids_and_embeddings()
nearest_neighbors = find_nearest_neighbors(ids_embeddings)
for apartment_id, nearest_neighbor_id in nearest_neighbors.items():
    print(f"Apartment ID {apartment_id} is most similar to Apartment ID {nearest_neighbor_id}")
plot_embeddings(ids_embeddings)
