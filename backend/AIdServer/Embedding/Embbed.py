import sqlite3
import numpy as np
from  backend.AIdServer.utils.db_utils import adapt_array, convert_array
from backend.AIdServer.Embedding.get_embedding import get_embedding


def create_connection():
    # register the adapter and converter for numpy array
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("array", convert_array)

    con = sqlite3.connect("backend/AIdServer/apartmentsAId.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()

    return con, cur

def insert_embeddings(con, cur):
    embedding = None
    #Selects apartments where there is a description and have not yet been embedded
    cur.execute("SELECT ApartmentId, Description FROM Apartments WHERE Description IS NOT NULL AND TRIM(Description) != '' AND Embedding IS NULL")
    rows = cur.fetchall()
    for row in rows:
        apartment_id, description = row
        embedding = get_embedding(description)
        # Update the database with the embedding
        cur.execute("UPDATE Apartments SET Embedding = ? WHERE ApartmentId = ?", (embedding, apartment_id))    

    con.commit()
    con.close()

con, cur = create_connection()
insert_embeddings(con, cur)