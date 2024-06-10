
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
from backend.embedding.plot_embeddings import fetch_ids_and_embeddings

def find_nearest_neighbors(ids_embeddings):
    """Find the nearest neighbor for each apartment's pre-fetched embedding."""
    apartment_id, city_name, embedding = zip(*ids_embeddings)
    embeddings = np.array(embedding)

    # Compute cosine similarity matrix (since embeddings are normalized, this can be done using dot product)
    similarity_matrix = np.dot(embeddings, embeddings.T)
    np.fill_diagonal(similarity_matrix, -np.inf)  # to ignore self-similarity

    # Find the index of the maximum similarity for each embedding (excluding self)
    nearest_indices = np.argmax(similarity_matrix, axis=1)
    nearest_ids = [apartment_id[idx] for idx in nearest_indices]
    
    return dict(zip(apartment_id, nearest_ids))

def display_results_in_popup(nearest_neighbors):
    """Displays nearest neighbors in a pop-up window using tkinter."""
    window = tk.Tk()
    window.title("Nearest Neighbors Display")
    window.geometry('400x300')  # Set the size of the window

    txt = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    txt.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    for apartment_id, nearest_neighbor_id in nearest_neighbors.items():
        txt.insert(tk.END, f"Apartment ID {apartment_id} is most similar to Apartment ID {nearest_neighbor_id}\n")

    # Start the GUI event loop
    window.mainloop()

def example_closest(nearest_neighbors):
    """Displays nearest neighbor's text in a pop-up window using tkinter."""
    window = tk.Tk()
    window.title("Mutual Nearest Neighbors")
    window.geometry('400x300')  # Set the size of the window
    
    txt = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    txt.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
    # Check for mutual nearest neighbors
    mutual_neighbors = []
    for apartment_id, nearest_neighbor_id in nearest_neighbors.items():
        # Check if mutual
        if nearest_neighbors.get(nearest_neighbor_id) == apartment_id:
            if (nearest_neighbor_id, apartment_id) not in mutual_neighbors:
                mutual_neighbors.append((apartment_id, nearest_neighbor_id))
                txt.insert(tk.END, f"Apartment ID {apartment_id} and Apartment ID {nearest_neighbor_id} are mutual nearest neighbors.\n")

    # Start the GUI event loop
    window.mainloop()

# Fetch data and use functions
ids_embeddings = fetch_ids_and_embeddings()
nearest_neighbors = find_nearest_neighbors(ids_embeddings)
display_results_in_popup(nearest_neighbors)
example_closest(nearest_neighbors)
