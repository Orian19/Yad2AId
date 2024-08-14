# from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# from utils.refresh_apts_urls import refresh_apts_urls

# def run_refresh():
#     refresh_apts_urls()

# if __name__ == "__main__":
#     scheduler = BlockingScheduler()
#     # Schedule the job to run immediately and then every 48 hours
#     scheduler.add_job(run_refresh, 'interval', hours=48, next_run_time=datetime.now())
#     scheduler.start()


# from apscheduler.schedulers.blocking import BlockingScheduler
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from utils.refresh_apts_urls import refresh_apts_urls

# def run_apartments_spider():
#     process = CrawlerProcess(get_project_settings())
#     process.crawl('apartments_spider')  # Name of the spider
#     process.start()

# def run_description_spider():
#     process = CrawlerProcess(get_project_settings())
#     process.crawl('description_spider')  # Name of the spider
#     process.start()

# def run_spiders():
#     # Run the apartments_spider first
#     run_apartments_spider()
    
#     # Run the description_spider after the first spider completes
#     run_description_spider()

# if __name__ == "__main__":
#     scheduler = BlockingScheduler()

#     # Schedule the spider job to run every 24 hours
#     scheduler.add_job(run_spiders, 'interval', hours=24)
    
#     # Schedule the refresh_apts_urls job to run every 48 hours
#     scheduler.add_job(refresh_apts_urls, 'interval', hours=48)
    
#     scheduler.start()




from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from utils.refresh_apts_urls import refresh_apts_urls

def run_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the job to run immediately and then every 48 hours
    scheduler.add_job(refresh_apts_urls, 'interval', hours=72, next_run_time=datetime.now())
    scheduler.start()
    return scheduler  # Return the scheduler object

if __name__ == "__main__":
    scheduler = run_scheduler()
    
    # Keep the script running
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
