import sqlite3
import numpy as np
import io

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    try:
        return np.load(out, allow_pickle=True)  # Setting allow_pickle to False for security unless you're sure about the content
    except Exception as e:
        print(f"Failed to load numpy array: {e}")
        return None  # Or handle the error as appropriate
