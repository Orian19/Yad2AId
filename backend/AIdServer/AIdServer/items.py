# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AidserverItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    sqm = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
