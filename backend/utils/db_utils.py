import sqlite3
import numpy as np
import io


def adapt_array(arr):
    """
    adapt numpy array to binary format for SQLite
    :param arr: numpy array
    :return:
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    """
    convert binary format back to numpy array.
    :param text:
    :return: numpy array
    """
    out = io.BytesIO(text)
    out.seek(0)
    try:
        return np.load(out, allow_pickle=True)
    except Exception as e:
        print(f"Failed to load numpy array: {e}")
        return None


def create_connection():
    """
    create a connection to the SQLite database
    return: connection and cursor
    """
    # register the adapter and converter for numpy array
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("array", convert_array)

    connection = sqlite3.connect(r"C:\IdeaToReality\FinalProject\Yad2AId\backend\AIdServer\apartmentsAId.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    return connection, cursor


def get_apt_urls():
    """
    get all the apartment urls from the database
    return: list of urls
    """
    con, cur = create_connection()
    cur.execute("SELECT Url FROM Apartments WHERE description IS NULL OR description = ''")
    urls = cur.fetchall()
    con.close()
    return [url[0] for url in urls]  # because each URL is returned is a tuple


def remove_apt_by_url(apartment_url: str):
    """
    remove apartment by its url
    :param apartment_url: the url of the apartment
    """
    con, cur = create_connection()
    cur.execute("DELETE FROM Apartments WHERE Url = ?", (apartment_url,))
    con.commit()
    con.close()
