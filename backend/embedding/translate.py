from backend.embedding.get_embedding import translate_to_english
from backend.utils.db_utils import create_connection
import sqlite3

def update_city_names(db_path):
    con, cur = create_connection()

    # Select rows where CityNameEnglish is NULL
    cur.execute("SELECT CityId, CityName FROM Cities WHERE CityNameEnglish IS NULL")
    rows = cur.fetchall()

    # Update each row where CityNameEnglish is NULL
    for row in rows:
        city_id = row[0]
        city_name = row[1]
        city_name_english = translate_to_english(city_name)  # Translate the city name to English

        # Update the CityNameEnglish column
        cur.execute("UPDATE Cities SET CityNameEnglish = ? WHERE CityId = ?", (city_name_english, city_id))

    # Commit the changes and close the connection
    con.commit()
    con.close()

    print("City names updated successfully.")

# Update names
update_city_names('backend/AIdServer/apartmentsAId.db')
