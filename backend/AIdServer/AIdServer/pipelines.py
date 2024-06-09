# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import numpy as np
import io

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
        # register the adapter and converter for numpy array
        sqlite3.register_adapter(np.ndarray, self.adapt_array)
        sqlite3.register_converter("array", self.convert_array)

        self.connection = sqlite3.connect("apartmentsAId.db", detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        # self.cursor.execute("""DROP TABLE IF EXISTS apartments_tb""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT UNIQUE
                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Cities(
                        CityId INTEGER PRIMARY KEY AUTOINCREMENT,
                        CityName TEXT UNIQUE
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Apartments(
                        ApartmentId INTEGER PRIMARY KEY AUTOINCREMENT,
                        CityId INTEGER,
                        Price INTEGER,
                        Address TEXT UNIQUE,
                        Rooms INTEGER,
                        Floor INTEGER,
                        SQM INTEGER,
                        Description TEXT,
                        Image TEXT,
                        PaidAd BOOLEAN DEFAULT FALSE,
                        Url TEXT,
                        Embedding array,
                        FOREIGN KEY (CityId) REFERENCES Cities(CityId)
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

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS UserSeenApartments(
                                        UserId INTEGER,
                                        ApartmentId INTEGER,
                                        FOREIGN KEY (UserId) REFERENCES Users(UserId),
                                        FOREIGN KEY (ApartmentId) REFERENCES Apartments(ApartmentId),
                                        PRIMARY KEY (UserId, ApartmentId)
                                        )""")

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    @staticmethod
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

    @staticmethod
    def convert_array(text):
        """
        convert binary format back to numpy array.
        :param text:
        :return: numpy array
        """
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out, allow_pickle=True)

    @staticmethod
    def find_shortest_list_length(item, keys):
        """
        find the shortest list length in the item
        :param item:
        :param key:
        :return:
        """
        lengths = {k: len(item.get(k)) for k in keys}
        min_key = min(lengths, key=lengths.get)
        return lengths[min_key], min_key

    def get_or_create_city(self, city_name):
        """
        get or create city in the database
        :param city_name:
        :return: city id
        """
        self.cursor.execute("SELECT CityId FROM Cities WHERE CityName = ?", (city_name,))
        result = self.cursor.fetchone()
        if result:  # city exists
            return result[0]
        else:  # city does not exist
            self.cursor.execute("INSERT INTO Cities (CityName) VALUES (?)", (city_name,))
            return self.cursor.lastrowid

    def store_item(self, item):
        self.cursor.execute("""INSERT OR IGNORE INTO Users (Name) VALUES (?)""", (
            "Orian",
        ))

        min_len, key = self.find_shortest_list_length(item, ['city', 'price', 'address', 'rooms', 'floor', 'sqm', 'description', 'image', 'url'])

        for i in range(min_len):
            try:
                if item.get('description')[i] == []:
                    item.get('description')[i] = ''

                city_id = self.get_or_create_city(item.get('city')[i])
                self.cursor.execute(
                    """INSERT OR IGNORE INTO Apartments (CityId, Price, Address, Rooms, Floor, SQM, Description, Image, Url) VALUES (?,?,?,?,?,?,?,?,?)""", (
                        city_id,
                        item.get('price')[i],
                        item.get('address')[i],
                        item.get('rooms')[i],
                        item.get('floor')[i],
                        item.get('sqm')[i],
                        item.get('description')[i],
                        item.get('image')[i],
                        # item.get('paid_ad')[i],
                        item.get('url')[i]
                    ))
            except Exception as e:
                self.connection.commit()
                print(key)
                print(e)


        # self.cursor.execute("""INSERT INTO UserLikedApartments (UserId, ApartmentId) VALUES (?,?)""", (
        #     0,
        #     0
        # ))
        #
        # self.cursor.execute("""INSERT INTO UserDislikedApartments (UserId, ApartmentId) VALUES (?,?)""", (
        #     0,
        #     0
        # ))
        #
        # self.cursor.execute("""INSERT INTO UserSeenApartments (UserId, ApartmentId) VALUES (?,?)""", (
        #     0,
        #     0
        # ))

        self.connection.commit()
