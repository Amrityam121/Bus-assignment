# app/models.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    search_history = relationship("SearchHistory", back_populates="user")  # Add this line


class Bus(Base):
    __tablename__ = "buses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    date_of_journey = Column(DateTime, nullable=False)
    seats_available = Column(Integer, nullable=False)
    stops = Column(String)  

class SeatBlock(Base):
    __tablename__ = "seat_blocks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    bus_id = Column(String, ForeignKey("buses.id"))
    no_of_passengers = Column(Integer, nullable=False)
    pickup_point = Column(String, nullable=False)
    confirmed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id")) 
    bus = relationship("Bus")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    block_id = Column(String, ForeignKey("seat_blocks.id"))
    user_id = Column(String, ForeignKey("users.id"))  
    block = relationship("SeatBlock")

class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    date_of_journey = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="search_history")

