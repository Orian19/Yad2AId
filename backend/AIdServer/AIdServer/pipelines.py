# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AidserverPipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.create_connection()
        self.create_tables()
        # self.close_connection()  # todo: need to close connection somewhere

    def create_connection(self):
        self.connection = sqlite3.connect("apartmentsAId.db")
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        # self.cursor.execute("""DROP TABLE IF EXISTS apartments_tb""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT
                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Apartments(
                        ApartmentId INTEGER PRIMARY KEY AUTOINCREMENT,
                        City TEXT,
                        Embedding INTEGER
                        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS UserLikedApartments(
                        UserId INTEGER,
                        ApartmentId INTEGER,
                        FOREIGN KEY (UserId) REFERENCES Users(UserId),
                        FOREIGN KEY (ApartmentId) REFERENCES Apartments(ApartmentId),
                        PRIMARY KEY (UserId, ApartmentId)
                        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS UserDislikedApartments(
                                UserId INTEGER,
                                ApartmentId INTEGER,
                                FOREIGN KEY (UserId) REFERENCES Users(UserId),
                                FOREIGN KEY (ApartmentId) REFERENCES Apartments(ApartmentId),
                                PRIMARY KEY (UserId, ApartmentId)
                                )""")

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    def store_item(self, item):
        self.cursor.execute("""INSERT INTO Users (Name) VALUES (?)""", (
            "Orian",
        ))

        self.cursor.execute("""INSERT INTO Apartments (City, Embedding) VALUES (?,?)""", (
            item.get('title')[0],
            "0101"
        ))

        self.cursor.execute("""INSERT INTO UserLikedApartments (UserId, ApartmentId) VALUES (?,?)""", (
            0,
            0
        ))

        self.cursor.execute("""INSERT INTO UserDislikedApartments (UserId, ApartmentId) VALUES (?,?)""", (
            0,
            0
        ))

        self.connection.commit()
