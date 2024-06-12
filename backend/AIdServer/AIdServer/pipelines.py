# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from utils.db_utils import create_connection

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AidserverPipeline:
    def __init__(self):
        self.connection, self.cursor = create_connection()
        self.create_tables()
        # self.close_connection()  # todo: need to close connection somewhere

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
                        DescriptionEnglish TEXT,
                        LastUpdated Date,
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
    def find_shortest_list_length(item, keys):
        """
        find the shortest list length in the item
        :param item:
        :param keys:
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
        if item.get('description'):  # update the description
            self.cursor.execute("""
            UPDATE Apartments
            SET Description = ?
            WHERE Url = ? AND (Description IS NULL OR Description = '')
            """, (item.get('description'), item.get('url')))
        else:  # insert the item (apartment)
            self.cursor.execute("""INSERT OR IGNORE INTO Users (Name) VALUES (?)""", (
                "Orian",
            ))

            min_len, key = self.find_shortest_list_length(item,
                                            ['city', 'price', 'address', 'rooms', 'floor', 'sqm', 'image', 'url'])

            for i in range(min_len):
                try:
                    # if item.get('description')[i] == []:
                    #     item.get('description')[i] = ''

                    city_id = self.get_or_create_city(item.get('city')[i])
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    self.cursor.execute(
                        """INSERT OR IGNORE INTO Apartments 
                        (CityId, Price, Address, Rooms, Floor, SQM, Image, Url, LastUpdated) VALUES 
                        (?, ?,?,?,?,?,?,?,?)""",
                        (
                            city_id,
                            item.get('price')[i],
                            item.get('address')[i],
                            item.get('rooms')[i],
                            item.get('floor')[i],
                            item.get('sqm')[i],
                            # item.get('description')[i],
                            item.get('image')[i],
                            # item.get('paid_ad')[i],
                            item.get('url')[i],
                            current_date
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
