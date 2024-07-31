from utils.db_utils import create_connection
from embedding.create_embedding import get_embedding


def insert_embeddings(con, cur):
    embedding = None
    # Selects apartments where there is a description and have not yet been embedded
    cur.execute(
        "SELECT ApartmentId, DescriptionEnglish FROM Apartments WHERE DescriptionEnglish IS NOT NULL AND TRIM(DescriptionEnglish) != '' AND Embedding IS NULL")
    rows = cur.fetchall()
    for row in rows:
        apartment_id, description_english = row
        embedding = get_embedding(description_english)
        # Update the database with the embedding
        cur.execute("UPDATE Apartments SET Embedding = ? WHERE ApartmentId = ?", (embedding, apartment_id))

    con.commit()
    con.close()


con, cur = create_connection()
insert_embeddings(con, cur)
