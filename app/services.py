# app/services.py
from sqlalchemy.orm import Session
from sqlalchemy import exc
from . import crud, schemas, models

def search_buses_service(db: Session, search_request: schemas.BusSearchRequest,user_id):
    buses = crud.search_buses(db, search_request)
    crud.create_search_history(db, search_request,str(user_id))
    return buses

def block_seats_service(db: Session, block_request: schemas.SeatBlockRequest, user_id: str):
    try:
        bus = crud.get_bus_for_update(db, block_request.bus_id, block_request.date_of_journey, block_request.start_time)
        
        if not bus:
            raise ValueError("Invalid bus ID or no bus available for the selected date and time.")

        seat_block = crud.block_seats(db, bus, block_request, user_id) 
        return seat_block

    except exc.SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"An error occurred while blocking seats: {str(e)}")


def book_ticket_service(db: Session, booking_request: schemas.BookTicketRequest, user_id: str):
    seat_block = db.query(models.SeatBlock).filter(models.SeatBlock.id == booking_request.blocking_id, models.SeatBlock.user_id == user_id).first()  # Check user ID
    
    if not seat_block:
        raise ValueError("Invalid blocking ID or you do not have access to this block.")
    
    if seat_block.confirmed:
        raise ValueError("This block has already been booked.")
    
    seat_block.confirmed = True
    db.add(seat_block)
    
    booking = models.Booking(block_id=seat_block.id, user_id=user_id)  # Include user ID if necessary
    db.add(booking)
    
    db.commit()
    db.refresh(booking)
    
    return booking