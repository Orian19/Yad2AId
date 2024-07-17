from datetime import datetime
import json
import math
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from schemas import Swipe, User, AptFilter
from utils.db_utils import create_connection



app = FastAPI()

allowed_origin = os.getenv('CORS_ORIGIN', 'http://localhost:3000')
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

    def filter_apts(self, user:User, apt_filter: AptFilter):
        """
        filter apartments by price, location, etc. from the db
        :return: list of relevant apartments - never seen before + not swiped left on
        """
        pass

    def find_best_apt_match(self, user: User, apt_filter: AptFilter, swipe: Swipe):
        """
        use the embeddings of the apartments and the user's swipes to find the best apartment match
        :return: best apartment match
        """
        filtered_apts = self.filter_apts(user, apt_filter)
        if not filtered_apts:
            return None


        # self.get_trip_suggestions()
        #
        # flights = {}  # cheapest
        # hotels = {}  # most expensive (budget is after selecting the flight)
        # for destination in self.possible_destinations:
        #     cheapest_outbound_flight = self.get_outbound_flight(destination)
        #     cheapest_inbound_flight = self.get_inbound_flight(destination)
        #     cheapest_outbound_flight_price = cheapest_outbound_flight.get(next(iter(cheapest_outbound_flight)))['price']
        #     cheapest_inbound_flight_price = cheapest_inbound_flight.get(next(iter(cheapest_inbound_flight)))['price']
        #     total_cheapest_flight_price = cheapest_outbound_flight_price + cheapest_inbound_flight_price
        #     if total_cheapest_flight_price >= self.budget:
        #         print("\nYou can't afford a trip to any of the suggested locations\n")
        #         exit()
        #     flights.update(cheapest_outbound_flight)
        #     flights.update({next(iter(cheapest_inbound_flight))+"_in": cheapest_inbound_flight.get(next(iter(cheapest_inbound_flight)))})
        #
        #     expensive_hotel = self.get_hotel(destination, self.duration, int(self.budget - total_cheapest_flight_price))
        #     hotels.update(expensive_hotel)
        #
        #     # cheapest_flight_key = min(flights, key=lambda k: flights[k]['price'])
        #     # most_expensive_hotel_key = max(hotels, key=lambda k: hotels[k]['prices'][0]['rate_per_night']['extracted_lowest'])
        #     most_expensive_hotel_price = expensive_hotel.get(next(iter(
        #         expensive_hotel)))['rate_per_night']['extracted_lowest']
        #     total_cost = total_cheapest_flight_price + most_expensive_hotel_price * self.duration
        #     self.travel_options.append({
        #         "destination": destination,
        #         "flight": [cheapest_outbound_flight, cheapest_inbound_flight],
        #         "hotel": expensive_hotel,
        #         "total_cost": total_cost,
        #     })


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

    # global apt
    # apt = TripPlan()
    # apt.get_user_trip_preferences(user_pref)
    # apt.get_travel_options()
    # if not apt.travel_options:
    #     raise HTTPException(status_code=404, detail="Data not found - Trip Options")
    # return apt.travel_options
