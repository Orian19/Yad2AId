import sqlite3
from schemas import Swipe, User, AptFilter

class UserInformation:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor 
    
    def get_user_id(self, user_name: str):
        """
        get the user_id based on the user_name
        :param user_name: name of the user
        :return: user_id
        """
        query = f"""
            SELECT UserId
            FROM Users
            WHERE Name = ?
        """
        self.cursor.execute(query, (user_name,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None
    
    def login_user(self, user: User):
        """
        Log in the user. If the user doesn't exist, create a new entry.
        :param user: User object containing the user_name
        :return: None
        """
        # Check if the user already exists
        query = """
            SELECT UserId
            FROM Users
            WHERE Name = ?
        """
        self.cursor.execute(query, (user.user_name,))
        result = self.cursor.fetchone()

        if result:
            # User exists, no action needed
            print(f"User '{user.user_name}' logged in successfully.")
        else:
            # User doesn't exist, create a new entry
            insert_query = """
                INSERT INTO Users (Name)
                VALUES (?)
            """
            self.cursor.execute(insert_query, (user.user_name,))
            self.connection.commit()
            print(f"New user '{user.user_name}' created and logged in successfully.")
    
    def getUserApts(self, user: User, liked: bool):
        """
        Get all apartments liked by the user, including their details.
        :param user: User object containing the user_name
        :return: List of dictionaries containing apartment details
        """
        user_id = self.get_user_id(user.user_name)
    
        if user_id is None:
            return []  # Return an empty list if the user doesn't exist
        if liked:
            query = """
                SELECT a.ApartmentId, a.Address, c.CityName, a.Url
                FROM UserLikedApartments ula
                JOIN Apartments a ON ula.ApartmentId = a.ApartmentId
                JOIN Cities c ON a.CityId = c.CityId
                WHERE ula.UserId = ?
            """
        else: 
            query = """
                SELECT a.ApartmentId, a.Address, c.CityName, a.Url
                FROM UserDislikedApartments ula
                JOIN Apartments a ON ula.ApartmentId = a.ApartmentId
                JOIN Cities c ON a.CityId = c.CityId
                WHERE ula.UserId = ?
            """
    
        self.cursor.execute(query, (user_id,))
        liked_apartments = self.cursor.fetchall()
    
        # Convert the results to a list of dictionaries
        apartment_details = [
            {
                "id": apartment[0],
                "address": apartment[1],
                "city": apartment[2],
                "url": apartment[3]
            }
            for apartment in liked_apartments
        ]
    
        return apartment_details
    
    def updateUserLikedApts(self, apt_id):
        """
        Remove the apartment with the given id from the user's liked apartments in the SQLite database.

        :param apt_id: The ID of the apartment to remove.
        """

        try:
            self.cursor.execute("DELETE FROM UserLikedApartments WHERE ApartmentId = ?", (apt_id,))
            self.connection.commit()
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        

    def updateUserDislikedApts(self, apt_id):
        """
        Remove the apartment with the given id from the user's disliked apartments in the SQLite database.

        :param apt_id: The ID of the apartment to remove.
        """
        try:
            self.cursor.execute("DELETE FROM UserDislikedApartments WHERE ApartmentId = ?", (apt_id,))
            self.connection.commit()
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        