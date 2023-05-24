# Create models for provided data

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderTiming(BaseModel):
    order_id : int
    departed : datetime
    picked_up : datetime
    delivered : datetime

class GeoData(BaseModel):
    order_id: int
    driver_id: int	
    shift_id: int
    origin_id: Optional[int]
    pickup_id: int
    destination_id: int
    distance: Optional[int]
    lat_x: Optional[float]
    lng_x: Optional[float]
    lat_y: Optional[float]
    lng_y: Optional[float]
    lat: float
    lng: float

class Address(BaseModel):
    driver_id:int 
    area_id: int
    address_id: int
    lat	: float
    lng: float

class ValidatedData(BaseModel):
    order_timing : List[OrderTiming]
    geo_data : List[GeoData]
    address : List[Address]