import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Bus  
import random

DATABASE_URL = "postgresql://user:123@db/booking"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Sample Data Generation
def generate_dummy_buses(num_buses=10):
    """Generates a list of dummy bus records with random data."""
    sources = ["CityA", "CityB", "CityC", "CityD"]
    destinations = ["CityE", "CityF", "CityG", "CityH"]
    stops = ["Stop1", "Stop2", "Stop3", "Stop4", "Stop5"]
    
    buses = []
    for i in range(num_buses):
        source = random.choice(sources)
        destination = random.choice([d for d in destinations if d != source]) 
        start_time = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"  
        date_of_journey = datetime.utcnow() + timedelta(days=random.randint(1, 30))  
        seats_available = random.randint(10, 50)  
        route_stops = random.sample(stops, random.randint(2, len(stops)))  
        
        bus = Bus(
            source=source,
            destination=destination,
            start_time=start_time,
            date_of_journey=date_of_journey,
            seats_available=seats_available,
            stops=",".join(route_stops) 
        )
        buses.append(bus)
    return buses


def insert_dummy_buses():
    """Inserts dummy bus data into the buses table."""
    session = SessionLocal()
    try:
        buses = generate_dummy_buses()
        session.add_all(buses)
        session.commit()
        print(f"Inserted {len(buses)} dummy buses into the buses table.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_dummy_buses()
