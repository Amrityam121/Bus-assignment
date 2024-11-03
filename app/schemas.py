# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr

class BusSearchRequest(BaseModel):
    source: str
    destination: str
    date_of_journey: datetime

class BusResponse(BaseModel):
    id: str
    source: str
    destination: str
    start_time: str
    seats_available: int
    stops: List[str]

class SeatBlockRequest(BaseModel):
    bus_id: str
    no_of_passengers: int
    pickup_point: str
    date_of_journey: datetime
    start_time: str

class SeatBlockResponse(BaseModel):
    blocking_id: str

class BookTicketRequest(BaseModel):
    blocking_id: str

class BookTicketResponse(BaseModel):
    booking_id: str

class SearchHistoryResponse(BaseModel):
    id: str
    source: str
    destination: str
    date_of_journey: datetime
    timestamp: datetime

class SeatBlockHistoryResponse(BaseModel):
    blocking_id: str
    bus_id: str
    no_of_passengers: int
    pickup_point: str

class BookingHistoryResponse(BaseModel):
    booking_id: str
    blocking_id: str
