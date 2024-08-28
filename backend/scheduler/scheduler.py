# import sys
# import os
# from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# from scrapy.settings import Settings
# from scrapy.crawler import CrawlerProcess
#
# # Add the parent directory to sys.path to allow imports from sibling directories
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
#
# from utils.db_utils import create_connection
# from embedding.update_english_columns import update_english_description_column
# from embedding.insert_embedding import insert_embeddings
# from utils.refresh_apts_urls import refresh_apts_urls
#
# import logging
#
# # Configure logging to write to a file
# logging.basicConfig(filename='scheduler.out', level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
#
# # Define the path to the AIdServer directory
# AID_SERVER_PATH = os.path.join(parent_dir, "AIdServer")
# print(f"AIdServer path: {AID_SERVER_PATH}")
#
#
# # Ensure that the PYTHONPATH is correctly set
# def setup_pythonpath():
#     sys.path.append(AID_SERVER_PATH)
#
#
# def run_scrapy_spider(spider_name):
#     print(f"Running {spider_name} spider...")
#
#     # Set up Scrapy settings manually
#     scrapy_settings = Settings()
#     scrapy_settings.setmodule('AIdServer.AIdServer.settings')
#
#     # Manually set the spider modules and pipelines to the correct path
#     scrapy_settings.set('SPIDER_MODULES', ['AIdServer.AIdServer.spiders'])
#     scrapy_settings.set('ITEM_PIPELINES', {
#         'AIdServer.AIdServer.pipelines.AidserverPipeline': 300,  # Replace with your actual pipeline class
#     })
#
#     # Initialize and run the Scrapy process
#     process = CrawlerProcess(settings=scrapy_settings)
#     process.crawl(spider_name)
#     process.start()
#
#
# def update_database():
#     print("Starting database update...")
#
#     # 0. Remove apartments that no longer exist
#     refresh_apts_urls()
#
#     # 1. Run apartment crawler to get new apartments
#     # run_scrapy_spider("apartments")
#
#     # 2. Run description crawler to get descriptions of apartments
#     run_scrapy_spider("descriptions")
#
#     # Create connection to the database
#     con, cur = create_connection()
#
#     # 3. Update columns to English
#     update_english_description_column(con, cur)
#
#     # 4. After the update is complete, embed new apartments
#     insert_embeddings(con, cur)
#     con.close()
#
#     print("Database update completed.")
#
#
# # Configure the scheduler
# scheduler = BlockingScheduler()
#
# # Schedule the job to run every 72 hours
# scheduler.add_job(update_database, 'interval', hours=72, next_run_time=datetime.now())
#
# if __name__ == "__main__":
#     print("Starting scheduler...")
#     try:
#         setup_pythonpath()
#
#         # Print the current PYTHONPATH to debug
#         print("Current PYTHONPATH:", sys.path)
#
#         # Attempt to import AIdServer.settings manually to check if the import works
#         try:
#             import AIdServer.AIdServer.settings
#
#             print("AIdServer.AIdServer.settings imported successfully")
#         except ModuleNotFoundError as e:
#             print(f"Import failed: {e}")
#
#         # Start the scheduler
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()


import sys
import os
import logging

from twisted.internet import asyncioreactor
asyncioreactor.install()

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.db_utils import create_connection
from embedding.update_english_columns import update_english_description_column
from embedding.insert_embedding import insert_embeddings
from utils.refresh_apts_urls import refresh_apts_urls

# Define the path to the AIdServer directory
AID_SERVER_PATH = os.path.join(parent_dir, "AIdServer")
print(f"AIdServer path: {AID_SERVER_PATH}")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_pythonpath():
    sys.path.append(AID_SERVER_PATH)


@defer.inlineCallbacks
def run_spiders():
    logging.info("Running spiders sequentially...")

    # Configure logging for Scrapy
    configure_logging()

    # Set up Scrapy settings
    from scrapy.settings import Settings
    from scrapy.crawler import CrawlerRunner
    from AIdServer.AIdServer.spiders.apartments_spider import ApartmentsSpider
    from AIdServer.AIdServer.spiders.description_spider import DescriptionsSpider

    scrapy_settings = Settings()
    scrapy_settings.setmodule('AIdServer.AIdServer.settings')
    scrapy_settings.set('SPIDER_MODULES', ['AIdServer.AIdServer.spiders'])
    scrapy_settings.set('ITEM_PIPELINES', {
        'AIdServer.AIdServer.pipelines.AidserverPipeline': 300,
    })

    runner = CrawlerRunner(settings=scrapy_settings)

    # Run spiders sequentially
    yield runner.crawl(ApartmentsSpider)
    yield runner.crawl(DescriptionsSpider)

    reactor.stop()


def update_database():
    logging.info("Starting database update...")

    # 0. Remove apartments that no longer exist
    refresh_apts_urls()

    # 1. Run the spiders sequentially
    setup_pythonpath()
    reactor.callWhenRunning(run_spiders)
    reactor.run()

    # 2. Create connection to the database
    con, cur = create_connection()

    # 3. Update columns to English
    update_english_description_column(con, cur)

    # 4. After the update is complete, embed new apartments
    insert_embeddings(con, cur)
    con.close()

    logging.info("Database update completed.")


# Configure the scheduler
scheduler = BlockingScheduler()

scheduler.add_job(update_database, 'interval', hours=48, next_run_time=datetime.now())

if __name__ == "__main__":
    logging.info("Starting scheduler...")
    try:
        # Start the scheduler
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down scheduler")
        scheduler.shutdown()

