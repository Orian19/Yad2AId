from concurrent.futures import ThreadPoolExecutor
from db_utils import create_connection
import requests


def check_url(apt_id, url):
    """
    Check if the url is valid (opens up a page and not a 404 page)
    If not, remove the apartment from the database
    """
    connection, cursor = create_connection()
    if not url:
        return
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Removing apartment with ID {apt_id} and URL {url}")
            cursor.execute("DELETE FROM Apartments WHERE ApartmentId = ?", (apt_id,))
            connection.commit()
    except Exception as e:
        print(f"Failed to load URL {url}: {e}")


def refresh_apts_urls():
    """
    Remove from db all apartments that their url isn't valid anymore
    Refresh the urls of the apartments
    """
    connection, cursor = create_connection()
    cursor.execute("""
        SELECT ApartmentId, Url
        FROM Apartments
    """)
    apt_urls = cursor.fetchall()

    # Use a ThreadPoolExecutor to check the URLs concurrently
    with ThreadPoolExecutor() as executor:
        for apt_id, url in apt_urls:
            executor.submit(check_url, apt_id, url)

    connection.close()


refresh_apts_urls()
