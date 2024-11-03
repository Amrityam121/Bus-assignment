# app/crud.py
from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas

def search_buses(db: Session, search: schemas.BusSearchRequest):
    buses = db.query(models.Bus).filter(
        models.Bus.source == search.source,
        models.Bus.destination == search.destination,
        models.Bus.date_of_journey == search.date_of_journey
    ).all()
    return [
        {
            "id": bus.id,
            "source": bus.source,
            "destination": bus.destination,
            "seats_available": bus.seats_available,
            "start_time" : bus.start_time,
            "stops": bus.stops.split(",") if bus.stops else []  # Convert string to list
        }
        for bus in buses
    ]

def create_search_history(db: Session, search: schemas.BusSearchRequest, user_id: str):
    search_history = models.SearchHistory(
        source=search.source,
        destination=search.destination,
        date_of_journey=search.date_of_journey,
        user_id=user_id  # Save the user ID
    )
    db.add(search_history)
    db.commit()
    db.refresh(search_history)
    return search_history



def get_search_history(db: Session, user_id: str):
    return db.query(models.SearchHistory).filter(models.SearchHistory.user_id == user_id).all()


def get_bus_for_update(db: Session, bus_id: str, date_of_journey: datetime, start_time: str):
    return db.query(models.Bus).filter(
        models.Bus.id == bus_id,
        models.Bus.date_of_journey == date_of_journey,
        models.Bus.start_time == start_time
    ).with_for_update().first()

def block_seats(db: Session, bus: models.Bus, block_request: schemas.SeatBlockRequest, user_id: str):
    if block_request.no_of_passengers > bus.seats_available:
        raise ValueError("Insufficient seats available.")
    
    bus.seats_available -= block_request.no_of_passengers
    db.add(bus)

    seat_block = models.SeatBlock(
        bus_id=bus.id,
        no_of_passengers=block_request.no_of_passengers,
        pickup_point=block_request.pickup_point,
        user_id=user_id  # Set user ID here
    )
    db.add(seat_block)
    db.commit()
    db.refresh(seat_block)
    return seat_block

def book_ticket(db: Session, booking_request: schemas.BookTicketRequest):
    block = db.query(models.SeatBlock).filter(models.SeatBlock.id == booking_request.blocking_id).first()
    if block:
        booking = models.Booking(block_id=block.id)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
    return None





def get_block_history(db: Session, user_id: str):
    return db.query(models.SeatBlock).filter(models.SeatBlock.user_id == user_id).all()

def get_booking_history(db: Session, user_id: str):
    return db.query(models.Booking).join(models.SeatBlock).filter(models.SeatBlock.user_id == user_id).all()