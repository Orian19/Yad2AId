from backend.embedding.create_embedding import translate_to_english
from backend.utils.db_utils import create_connection
import sqlite3

def update_english_city_names_column(con, cur):
    
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
    print("City names updated successfully.")
    
def update_english_description_column(conn, cursor):

    # Fetch descriptions that need translation
    cursor.execute('''
        SELECT ApartmentId, Description FROM Apartments
        WHERE DescriptionEnglish IS NULL OR DescriptionEnglish = '';
    ''')
    apartments = cursor.fetchall()
    
    # Translate descriptions and update the database
    for apartment_id, description in apartments:
        english_description = translate_to_english(description)
        cursor.execute('''
            UPDATE Apartments
            SET DescriptionEnglish = ?
            WHERE ApartmentId = ?;
        ''', (english_description, apartment_id))
    
    # Commit changes and close the connection
    conn.commit()
    print("English descriptions updated successfully.")

# Example usage
con, cur = create_connection()
#update_english_description_column(con, cur)
#update_english_city_names_column(con, cur)
con.close()
