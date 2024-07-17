from pydantic import BaseModel, Field


class User(BaseModel):
    """
    user preferences for the trip - using pydantic to validate data (type and context wise)
    """
    model_config = {
        "extra": "forbid",  # not allowing attributes that are not defined here to be sent from the client
    }
    user_name: str = Field(..., description="user name")


class Swipe(BaseModel):
    """
    swipe left or right - user liked or disliked the apartment
    """
    model_config = {
        "extra": "forbid",  # not allowing attributes that are not defined here to be sent from the client
    }
    swipe: int = Field(examples=[0, 1], description="swipe left or right")


class AptFilter(BaseModel):
    """
    filter apartments by price, location, etc.
    """
    model_config = {
        "extra": "forbid",  # not allowing attributes that are not defined here to be sent from the client
    }
    price: int = Field(..., description="price range")
    city: str = Field(..., description="city")
    sqm: int = Field(..., description="size of the apartment in SQM")
    rooms: int = Field(..., description="number of rooms")
    # elevator: bool = Field(..., description="elevator in the building")
    # parking: bool = Field(..., description="parking in the building")
    # balcony: bool = Field(..., description="balcony in the apartment")
    # air_conditioning: bool = Field(..., description="air conditioning in the apartment")
    # heating: bool = Field(..., description="heating in the apartment")
    # furnished: bool = Field(..., description="furnished apartment")
    # storage: bool = Field(..., description="storage in the building")
    # date: str = Field(..., description="date of the apartment")
