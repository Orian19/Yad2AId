# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AidserverPipeline:
    def __init__(self):
        self.conn = None
        self.curr = None
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("apartmentsAId.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS apartments_tb""")
        self.curr.execute("""create table apartments_tb(
                title text
                )""")

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    def store_item(self, item):
        self.curr.execute("""insert into apartments_tb values (?)""", (
            item['title'][0],
        ))
        self.conn.commit()
