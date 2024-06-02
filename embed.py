import openai 
from sklearn.metrics.pairwise import cosine_similarity
from translate import translate_to_english
import numpy as np


OPENAI_API_KEY = 'sk-proj-FCEXpTYz85m73awMbiW5T3BlbkFJfDaS86ZuEMtq6XU60ymU'

def normalize_l2(x):
    x = np.array(x)
    if x.ndim == 1:
        norm = np.linalg.norm(x)
        if norm == 0:
            return x
        return x / norm
    else:
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
        return np.where(norm == 0, x, x / norm) 
    
def get_embedding(text_to_embed: dict, model):
    """
    Fetches the embedding for a given text using OpenAI's embedding model.

    Parameters:
    text_to_embed (str): The text string for which the embedding is required.

    Returns:
    list: A list of floats representing the embedding of the text.
    """
    
    openai.api_key = OPENAI_API_KEY
    text = str(text_to_embed)
    # Create an embedding for the specified text using the desired model
    response = openai.Embedding.create(
        input=text,
        model=model
    )

    # Extract and print the embedding
    embedding = response.data[0].embedding[:256]
    return normalize_l2(embedding)



def compare_strings(str1, str2, str3):
    """
    Compares three strings and determines which two are most similar
    based on their embeddings.

    Parameters:
    str1, str2, str3 (str): The strings to be compared.

    Returns:
    tuple: A tuple containing the two most similar strings and their similarity score.
    """
    # Get embeddings for each string
    emb1 = get_embedding(str1)
    emb2 = get_embedding(str2)
    emb3 = get_embedding(str3)

    # Calculate cosine similarity between each pair of embeddings
    sim12 = cosine_similarity([emb1], [emb2])[0][0]
    sim23 = cosine_similarity([emb2], [emb3])[0][0]
    sim13 = cosine_similarity([emb1], [emb3])[0][0]

    # Determine which pair of strings has the highest similarity
    max_sim = max(sim12, sim23, sim13)
    if max_sim == sim12:
        return (str1, str2, sim12)
    elif max_sim == sim23:
        return (str2, str3, sim23)
    else:
        return (str1, str3, sim13)

# Example usage


str1 = {
    "קומות בבניין": 3,
    "סה״כ תשלום חודשי": 3450,
    "ועד בית (לחודש)": 50,
    "ארנונה (לחודשיים)": 400,
    "מ״ר בנוי": 57,
    "חניות": "ללא",
    "תאריך כניסה": "כניסה מידית"
}
str2 =  {
    "קומות בבניין": 5,
    "סה״כ תשלום חודשי": 4200,
    "ועד בית (לחודש)": 75,
    "ארנונה (לחודשיים)": 600,
    "מ״ר בנוי": 75,
    "חניות": "אחת",
    "תאריך כניסה": "מיידי או לפי הסכם"
}
str3 = {
    "קומות בבניין": 2,
    "סה״כ תשלום חודשי": 2900,
    "ועד בית (לחודש)": 30,
    "ארנונה (לחודשיים)": 300,
    "מ״ר בנוי": 45,
    "חניות": "שתיים",
    "תאריך כניסה": "כניסה תוך חודש"
}

most_similar_strings, second_string, sim_score = compare_strings(translate_to_english(str1), translate_to_english(str2), translate_to_english(str3))
print(f"The most similar strings are: {most_similar_strings} and {second_string}, with a similarity score of {sim_score:.2f}")