from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from backend.utils.db_utils import create_connection
import tkinter as tk
from tkinter import scrolledtext


def fetch_ids_and_embeddings():
    """Fetches apartment IDs, city names, and pre-calculated embedding from the SQLite database."""
    con, cur = create_connection()
    cur.execute("""
        SELECT a.ApartmentId, c.CityNameEnglish, a.Embedding 
        FROM Apartments a 
        JOIN Cities c ON a.CityId = c.CityId 
        WHERE a.Description IS NOT NULL AND TRIM(a.Description) != '' AND a.Embedding IS NOT NULL
    """)
    result = cur.fetchall()
    ids_embeddings = []
    expected_shape = None

    for row in result:
        apartment_id, city_name, embedding = row[0], row[1], row[2]
        if embedding is None:
            print(f"Warning: Embedding for Apartment ID {apartment_id} is None")
            continue
        if expected_shape is None:
            expected_shape = embedding.shape
        if embedding.shape == expected_shape:
            ids_embeddings.append((apartment_id, (city_name), embedding))
        else:
            print(f"Warning: Embedding shape {embedding.shape} for Apartment ID {apartment_id} does not match expected {expected_shape}")
    con.close()
    return ids_embeddings

def plot_embeddings(ids_embeddings, cities_to_include):
    """Plots pre-fetched embeddings with interactive tooltips showing IDs, colored by city name, filtered by specified cities."""
    # Filter embeddings for specified cities
    filtered_embeddings = [entry for entry in ids_embeddings if entry[1] in cities_to_include]
    if not filtered_embeddings:
        print("No embeddings found for the specified cities.")
        return

    ids, city_names, embeddings = zip(*filtered_embeddings)
    embeddings = np.array(embeddings)

    tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Create a unique list of cities and sort it to maintain consistency
    unique_cities = sorted(set(city_names))
    colors = plt.cm.get_cmap('tab20', len(unique_cities))  # Select a colormap
    city_to_color = {city: colors(unique_cities.index(city)) for city in unique_cities}

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1],
                         c=[city_to_color[city] for city in city_names],  # Map city names to colors
                         label=[city for city in city_names])

    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=city,
                              markerfacecolor=city_to_color[city], markersize=10)
                       for city in unique_cities]
    ax.legend(handles=legend_elements, title="Cities")

    # Annotation for hover effect
    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = scatter.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f"Apartment ID: {ids[ind['ind'][0]]}, City: {city_names[ind['ind'][0]]}"
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

    # Connect the hover event
    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.title('Apartment Embeddings by City')
    plt.show()


# Example usage
ids_embeddings = fetch_ids_and_embeddings()
cities_to_plot = ["Ashkelon", "Tel Aviv Jaffa", "Haifa", "Bat Yam", "Ramat Gan", "Beer Sheva", "Netanya", "Jerusalem", "Raanana", "Kfar Saba"]
#plot_embeddings(ids_embeddings, cities_to_plot)
