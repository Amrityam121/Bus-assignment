# app/main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, get_db
from . import models, schemas, crud, services, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/search_buses", response_model=List[schemas.BusResponse])
def search_buses(search_request: schemas.BusSearchRequest, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    buses = services.search_buses_service(db, search_request,user.id)
    if not buses:
        raise HTTPException(status_code=404, detail="No buses available for the selected route and date.")
    return buses

@app.post("/block_seats", response_model=schemas.SeatBlockResponse)
def block_seats(block_request: schemas.SeatBlockRequest, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    try:
        seat_block = services.block_seats_service(db, block_request, user.id)  
        return {"blocking_id": seat_block.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  


@app.post("/book_ticket", response_model=schemas.BookTicketResponse)
def book_ticket(booking_request: schemas.BookTicketRequest, db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    try:
        booking = services.book_ticket_service(db, booking_request, user.id)  
        return {"booking_id": booking.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  

@app.get("/search_history", response_model=List[schemas.SearchHistoryResponse])
def get_search_history(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    search_history = crud.get_search_history(db, user.id)
    if not search_history:
        raise HTTPException(status_code=404, detail="No search history found.")
    return search_history


@app.get("/block_history", response_model=List[schemas.SeatBlockHistoryResponse])
def get_block_history(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    blocks = crud.get_block_history(db, user.id)  
    return [
        {
            "blocking_id": block.id,
            "bus_id": block.bus_id,
            "no_of_passengers": block.no_of_passengers,
            "pickup_point": block.pickup_point
        } for block in blocks
    ]

@app.get("/booking_history", response_model=List[schemas.BookingHistoryResponse])
def get_booking_history(db: Session = Depends(get_db), user: models.User = Depends(auth.get_current_user)):
    bookings = crud.get_booking_history(db, user.id)  
    return [
        {
            "booking_id": booking.id,
            "blocking_id": booking.block_id
        } for booking in bookings
    ]
