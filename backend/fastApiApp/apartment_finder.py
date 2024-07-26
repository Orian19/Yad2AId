from datetime import datetime
import json
import math
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from schemas import Swipe, User, AptFilter
from utils.db_utils import create_connection
from embedding.most_similar_apts import most_similar_apts

app = FastAPI()

allowed_origin = os.getenv('CORS_ORIGIN', 'http://localhost:8000')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AptFinder:
    def __init__(self):
        self.connection, self.cursor = create_connection()

    def filter_apts(self, user: User, apt_filter: AptFilter):
        """
        filter apartments by price, location, etc. from the db
        :return: list of relevant apartments ids - never seen before + not swiped left on
        """
        # extract user's preferences
        params = (user.user_name, apt_filter.city, apt_filter.price, apt_filter.sqm, apt_filter.rooms,
                  user.user_name, user.user_name)

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
               """

        # Execute the query
        self.cursor.execute(query, params)
        # Fetch the results
        filtered_apts = self.cursor.fetchall()
        filtered_apts = [apt_id[0] for apt_id in filtered_apts]
        return filtered_apts

    def find_best_apt_match(self, user: User, apt_filter: AptFilter, swipe: Swipe):
        """
        use the embeddings of the apartments and the user's swipes to find the best apartment match
        :return: best apartment match
        """
        filtered_apts = self.filter_apts(user, apt_filter)
        if not filtered_apts:
            return None

        best_match = most_similar_apts(filtered_apts)
        return best_match


# TODO: comment for testing purposes
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
    best_match = apt.find_best_apt_match(user, apt_filter, swipe)
    if not best_match:
        raise HTTPException(status_code=404, detail="Data not found - Apartment")
    return best_match

# TODO: uncomment for testing purposes
# if __name__ == "__main__":
#     apt = AptFinder()
# print(apt.find_best_apt_match(User(user_name="Orian"), AptFilter(city=" חיפה", price=10000, sqm=50, rooms=2), Swipe(swipe="right")))
