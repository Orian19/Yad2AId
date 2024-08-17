import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from backend.utils.db_utils import create_connection
from backend.embedding.update_english_columns import update_english_description_column
from backend.embedding.insert_embedding import insert_embeddings
from backend.utils.refresh_apts_urls import refresh_apts_urls

# Your function that updates the database
def update_database():
    print("Starting database update...")
    
    # 0. Remove apartments that no longer exist
    refresh_apts_urls()
        
    # 1. Run apartment crawler to get new apartments
    subprocess.run(["scrapy", "crawl", "apartments"])
    
    # 2. Run description crawler to get descriptions of apartments
    subprocess.run(["scrapy", "crawl", "descriptions"])
    
    # create connection to database
    con, cur = create_connection()
    
    # 3. Update columns to English
    update_english_description_column(con, cur)
    
    # 4. After the update is complete, embed new apartments
    insert_embeddings(con, cur)
    con.close()
    
    print("Database update completed.")

# Configure the scheduler
scheduler = BlockingScheduler()

# Schedule the job to run every 12 hours
scheduler.add_job(update_database, 'interval', minutes=1)

if __name__ == "__main__":
    print("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
