from datetime import datetime
import json
import math
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from schemas import Swipe, User, AptFilter
from backend.utils.db_utils import create_connection
from backend.embedding.most_similar_apts import most_similar_apts
from backend.utils.refresh_apts_urls import check_url

app = FastAPI()

# Fetch the allowed origin from the environment variable
allowed_origin = os.getenv('CORS_ORIGIN', '')

# Define other allowed origins
origins = [
    allowed_origin,
    "chrome-extension://*",
    "https://www.yad2.co.il",
    "https://www.yad2.co.il/realestate/forsale",
    "https://www.yad2.co.il/realestate/rent",

]

# Remove empty strings from the list
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AptFinder:
    def __init__(self):
        self.connection, self.cursor = create_connection()

    def get_apt_url(self, apt_id: int):
        """
        get the url of the apartment
        :param apt_id: apartment id
        :return: url of the apartment
        """
        query = f"""
            SELECT Url
            FROM Apartments
            WHERE ApartmentId = ?
        """

        self.cursor.execute(query, (apt_id,))
        url = self.cursor.fetchone()

        return url[0] if url else None

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

    def update_user_swipe(self, user_id: int, apt_id: int, swipe: Swipe):
        """
        update the user's swipe in the db
        update the UserLikedApartments or UserDislikedApartments tables
        :param user_id: user object
        :param apt_id: apartment id
        :param swipe: swipe object
        :return None
        """
        if swipe.swipe == "right":
            query = f"""
                INSERT INTO UserLikedApartments (UserId, ApartmentId)
                VALUES (?,?)
                ON CONFLICT (UserId, ApartmentId) DO NOTHING
            """
        else:
            query = f"""
                INSERT INTO UserDislikedApartments (UserId, ApartmentId)
                VALUES (?,?)
                ON CONFLICT (UserId, ApartmentId) DO NOTHING
            """

        self.cursor.execute(query, (user_id, apt_id))
        self.connection.commit()

    def filter_apts(self, user: User, apt_filter: AptFilter, swipe: Swipe):
        """
        Filter apartments by price, location, etc. from the database.
        :return: list of relevant apartment ids - never seen before + not swiped left on.
        """

        def format_city_name(city: str) -> str:
            city = city.strip()
            return f" {city}" if not city.startswith(" ") else city

        # Format the city name
        formatted_city = format_city_name(apt_filter.city)

        # Extract user's preferences
        params = (user.user_name, formatted_city, apt_filter.price, apt_filter.sqm, apt_filter.rooms,
                  user.user_name, user.user_name, swipe.apt_id)

        query = f"""
                SELECT a.ApartmentId
                FROM Apartments a
                JOIN Cities c ON a.CityId = c.CityId
                JOIN Users u ON u.UserId = (
                    SELECT u1.UserId 
                    FROM Users u1 
                    WHERE u1.Name = ?
                )
                WHERE c.CityName = ?
                AND a.Price <= ?
                AND a.SQM >= ?
                AND a.Rooms = ?
                AND a.ApartmentId NOT IN (
                    SELECT uda.ApartmentId
                    FROM UserDislikedApartments uda
                    WHERE uda.UserId = (
                        SELECT u2.UserId 
                        FROM Users u2 
                        WHERE u2.Name = ?
                    )
                )
                AND a.ApartmentId NOT IN (
                    SELECT ula.ApartmentId
                    FROM UserLikedApartments ula
                    WHERE ula.UserId = (
                        SELECT u3.UserId 
                        FROM Users u3 
                        WHERE u3.Name = ?
                    )
                )
                AND a.ApartmentId <> ?
               """

        # Execute the query
        self.cursor.execute(query, params)
        # Fetch the results
        filtered_apts = self.cursor.fetchall()
        filtered_apts = [apt_id[0] for apt_id in filtered_apts]

        return filtered_apts

    def find_best_apt_match(self, user: User, apt_filter: AptFilter, swipe: Swipe):
        """
        Use the embeddings of the apartments and the user's swipes to find the best apartment match.
        :return: URL of the best apartment match (specific standalone apartment page) and its ID.
        """
        # Initialize best_match_url and best_match_id
        best_match_url, best_match_id = None, None
        
        # Get filtered apartments IDs
        filtered_apts = self.filter_apts(user, apt_filter, swipe)
        
        # Keep trying until a valid URL is found
        while True:
            if not filtered_apts:
                return None, None  # No apartments found after filtering

            # Get the most similar apartment ID
            user_id = self.get_user_id(user.user_name)
            best_match_id = most_similar_apts(filtered_apts, user_id)

            # Update liked/disliked apartments
            if swipe.apt_id != 0:
                self.update_user_swipe(user_id, swipe.apt_id, swipe)

            # Get the URL of the best match
            best_match_url = self.get_apt_url(best_match_id)

            # Check if the URL is valid, if so, break the loop
            if check_url(best_match_id, best_match_url):
                break
            else:
                #remove faulty apartment_id from filtered_apts
                filtered_apts = [apt_id for apt_id in filtered_apts if apt_id != best_match_id]
                
                #edge case we ran out of apartments
                if not filtered_apts:
                    return None, None  # No apartments found after filtering
          
        return best_match_url, best_match_id

apt = AptFinder()


@app.post("/apartment/")
async def find_next_apt_match(user: User, apt_filter: AptFilter, swipe: Swipe):
    """
    find the next apartment match for the user based on the user's preferences and swipe
    :param user:
    :param apt_filter:
    :param swipe:
    :return:
    """
    global apt

    best_match, best_match_id = apt.find_best_apt_match(user, apt_filter, swipe)
    if best_match is None or best_match_id is None:
        print("No matches were found")
        raise HTTPException(status_code=404, detail="No matching apartment found")
    print(f"Url found: {best_match}")  # Testing
    print(f"Apt Id found: {best_match_id}")  # Testing
    return best_match, best_match_id

# TODO: uncomment for testing purposes
# if __name__ == "__main__":
#   apt = AptFinder()
# print(apt.find_best_apt_match(User(user_name="Orian"), AptFilter(city="הרצליה", price=10000, sqm=50, rooms=2), Swipe(apt_id=0, swipe="right", )))

