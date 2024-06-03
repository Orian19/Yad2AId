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
                Name TEXT
                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Apartments(
                        ApartmentId INTEGER PRIMARY KEY AUTOINCREMENT,
                        City TEXT,
                        Embedding array
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

    def store_item(self, item):
        embedding_example = np.asarray([0.09220705, 0.03540842, 0.00997891, 0.02807464, 0.00967811, 0.02960251
                                           , 0.08815819, 0.12238251, 0.09335295, 0.09511, 0.07635538, 0.10893724
                                           , 0.00721442, 0.01023674, 0.01172641, 0.071428, 0.05072533, 0.07173357
                                           , 0.09304738, 0.06237536, 0.0172936, 0.00586798, 0.01820077, 0.0059969
                                           , 0.01974774, 0.04927386, 0.05381927, 0.01400867, 0.01714081, 0.00093522
                                           , 0.09274181, 0.01124895, 0.01219432, 0.01957585, 0.04705844, 0.02165758
                                           , 0.057066, 0.09266541, 0.02035889, 0.11145823, 0.02824652, 0.0535137
                                           , 0.10282575, 0.03517924, 0.03137866, 0.03516014, 0.0725357, 0.04003023
                                           , 0.06814307, 0.01748458, 0.05137468, 0.00593483, 0.0321617, 0.01773286
                                           , 0.02696693, 0.07513308, 0.08265785, 0.20473479, 0.03155055, 0.10435362
                                           , 0.02345283, 0.03336489, 0.03061473, 0.02912505, 0.05496518, 0.15889864
                                           , 0.05064894, 0.10221461, 0.02421676, 0.01296781, 0.0095492, 0.00287192
                                           , 0.01449568, 0.07998408, 0.01307285, 0.02599291, 0.07536226, 0.02792185
                                           , 0.02219233, 0.05202403, 0.01639597, 0.07421636, 0.01042772, 0.04472844
                                           , 0.04144352, 0.06000715, 0.14682846, 0.23147253, 0.05217681, 0.07219193
                                           , 0.05080173, 0.01593761, 0.06749372, 0.02838021, 0.04820435, 0.03836868
                                           , 0.08265785, 0.01558429, 0.02561095, 0.00750089, 0.06191699, 0.0177997
                                           , 0.09701984, 0.04014482, 0.02037799, 0.01094338, 0.09518639, 0.0285903
                                           , 0.04980861, 0.00579159, 0.01271953, 0.01647236, 0.01947081, 0.00760594
                                           , 0.0136458, 0.01066645, 0.01149723, 0.07681374, 0.10374248, 0.01767556
                                           , 0.05294075, 0.20290134, 0.01309195, 0.17035768, 0.04900648, 0.03273465
                                           , 0.02249791, 0.01052321, 0.00454064, 0.0056388, 0.02440775, 0.02112282
                                           , 0.06944176, 0.06879241, 0.05809731, 0.03267735, 0.03577129, 0.00317272
                                           , 0.0059969, 0.02929694, 0.11932676, 0.12352841, 0.03338399, 0.05381927
                                           , 0.01083834, 0.06107666, 0.03023276, 0.0190029, 0.03072932, 0.01241396
                                           , 0.01547925, 0.00635022, 0.02522898, 0.07077865, 0.06925078, 0.0844149
                                           , 0.05064894, 0.05420124, 0.09258902, 0.02941153, 0.00286476, 0.01638642
                                           , 0.04904468, 0.01827716, 0.12329923, 0.02129471, 0.02431225, 0.01715036
                                           , 0.03668801, 0.0582501, 0.04923566, 0.07570603, 0.07952571, 0.02230692
                                           , 0.02673775, 0.00953965, 0.10649265, 0.08769983, 0.06222257, 0.08067162
                                           , 0.00767278, 0.11443758, 0.03911351, 0.0582883, 0.06596585, 0.04889189
                                           , 0.02540086, 0.10588149, 0.05057255, 0.01298691, 0.04667647, 0.08907491
                                           , 0.01744638, 0.07646997, 0.06268093, 0.04713484, 0.10809692, 0.0404122
                                           , 0.0522914, 0.06386503, 0.08235228, 0.05160386, 0.00406318, 0.0297744
                                           , 0.02089364, 0.02286078, 0.02526717, 0.06860143, 0.03632515, 0.00477221
                                           , 0.07379619, 0.07837981, 0.00967334, 0.04862451, 0.04354434, 0.02328094
                                           , 0.00113218, 0.05786813, 0.07425456, 0.0166156, 0.03558031, 0.12803564
                                           , 0.02356742, 0.00403931, 0.02070266, 0.03664982, 0.07245931, 0.13239006
                                           , 0.13536942, 0.0178761, 0.12406317, 0.05481239, 0.04625631, 0.01517367
                                           , 0.02360562, 0.00222616, 0.05481239, 0.09213065, 0.0511455, 0.00343532
                                           , 0.02158119, 0.06474355, 0.12039628, 0.07750128, 0.027368, 0.0892277
                                           , 0.01152588, 0.05660764, 0.08472047, 0.04350614, 0.02702423, 0.09045
                                           , 0.00585843, 0.04549238, 0.0963323, 0.0987769])

        self.cursor.execute("""INSERT INTO Users (Name) VALUES (?)""", (
            "Orian",
        ))

        self.cursor.execute("""INSERT INTO Apartments (City, Embedding) VALUES (?,?)""", (
            item.get('title')[0],
            embedding_example
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
