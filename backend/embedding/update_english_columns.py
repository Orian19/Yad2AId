from deep_translator import GoogleTranslator
from utils.db_utils import create_connection
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)


def translate_to_english(text: str) -> str:
    if not text:
        return ""  # Return empty string if input is empty

    translator = GoogleTranslator(source='auto', target='en')
    try:
        # Automatically detect the source language and translate to English
        translation = translator.translate(text)
        return translation
    except Exception as e:
        logging.error(f"Failed to translate text: {text[:30]}... Error: {str(e)}")
        return text  # Return original text on failure

def update_english_description_column(conn, cursor):

    # Fetch descriptions that need translation
    cursor.execute('''
        SELECT ApartmentId, Description FROM main.Apartments
        WHERE Description != 'empty' AND (DescriptionEnglish IS NULL OR DescriptionEnglish = '');
    ''')
    apartments = cursor.fetchall()

    # Translate descriptions and update the database
    for apartment_id, description in apartments:
        try:
            english_description = translate_to_english(description)
            cursor.execute('''
                UPDATE Apartments
                SET DescriptionEnglish = ?
                WHERE ApartmentId = ?;
            ''', (english_description, apartment_id))
            
            # Commit changes
            conn.commit()
        except Exception as e:
            logging.error(f"Database update failed for ApartmentId {apartment_id}: {str(e)}")

    logging.info("English descriptions updated successfully.")

# Example usage
#con, cur = create_connection()
#update_english_description_column(con, cur)
#con.close()
