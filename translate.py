import json
from googletrans import Translator, LANGUAGES

def translate_to_english(dict_text: dict):
    translator = Translator()
    str_text = str(dict_text)
    
    # Automatically detect the source language and translate to English
    translation = translator.translate(str_text, dest='en')
    
    corrected_json_string = translation.text.replace("'", '"').replace('“', '"').replace('”', '"')
    try:
        # Convert translated JSON string back to dictionary
        translated_dict = json.loads(corrected_json_string)
        return translated_dict
    
    except json.JSONDecodeError as e:
        return f"Failed to decode JSON: {e}"

