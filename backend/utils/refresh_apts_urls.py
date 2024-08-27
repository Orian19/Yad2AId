# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.db_utils import create_connection
from datetime import datetime, timedelta
import time

# chrome_options = Options()
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--window-size=1920x1080")

# Do not set headless mode since the website detects it
# driver = webdriver.Chrome(options=chrome_options)
# Add Firefox-specific options if needed
firefox_options = Options()
firefox_options.headless = False  # Set to True if you want to run headless

# Replace Chrome WebDriver with Firefox WebDriver
driver = webdriver.Firefox(options=firefox_options)

# Initialize a counter for removed apartments
removed_count = 0

def check_url(apt_id: int, url: str) -> bool:
    """
    Check if the URL is valid (opens up a page and not a 404 page)
    If not, remove the apartment from the database
    param apt_id: int, the apartment ID
    param url: str, the apartment URL
    return: bool, True if the URL is valid, False otherwise
    """
    global removed_count
    connection, cursor = create_connection()
    if not url:
        return
    if not url.startswith("http"):
        url = "https://" + url
    try:
        driver.get(url)
        page_content = driver.page_source.lower()

        blocked = "אנו מניחים שגולשים כאן בני אנוש"
        if blocked in page_content and "רכב" not in page_content:
            print(f"Request blocked, apartment ID {apt_id} and URL {url}")
            return False

        invalid_content = ["חיפשנו בכל מקום אבל אין לנו עמוד כזה", "כנראה שהלינק לא תקין או שהעמוד שחיפשת הוסר"]
        if any(keyword in page_content for keyword in invalid_content):
            print(f"Removing apartment with ID {apt_id} and URL {url} due to invalid content")
            cursor.execute("DELETE FROM Apartments WHERE ApartmentId = ?", (apt_id,))
            cursor.execute("DELETE FROM UserLikedApartments WHERE ApartmentId = ?", (apt_id,))
            cursor.execute("DELETE FROM UserDislikedApartments WHERE ApartmentId = ?", (apt_id,))
            connection.commit()
            removed_count += 1
            return False

        # Only update LastUpdated if not blocked
        current_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("UPDATE Apartments SET LastUpdated = ? WHERE ApartmentId = ?", (current_date, apt_id))
        connection.commit()
        print(f"Updated LastUpdated for apartment ID {apt_id} to {current_date}")
        return True

    except Exception as e:
        print(f"Error with apartment ID {apt_id} and URL {url}: {e}")
        return False

    finally:
        connection.close()

def refresh_apts_urls() -> None:
    """
    Remove from the database all apartments that their URL isn't valid anymore
    param: None
    return: None
    """
    connection, cursor = create_connection()
    # only check apartments that haven't been updated in the last 5 days
    five_days_ago = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT ApartmentId, Url
        FROM Apartments
        WHERE LastUpdated < ?
    """, (five_days_ago,))
    # connection, cursor = create_connection()
    # cursor.execute("""
    #     SELECT ApartmentId, Url
    #     FROM Apartments
    # """)
    apt_urls = cursor.fetchall()
    connection.close()

    # apt_urls = apt_urls[::-1]

    # Sequentially process each URL without threading
    for apt_id, url in apt_urls:
        check_url(apt_id, url)

    print(f"Total apartments removed: {removed_count}")

# refresh_apts_urls()
# driver.quit()
