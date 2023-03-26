import sys
sys.path.append("..")

from fastapi import HTTPException, Depends, APIRouter, Request
import models
from typing import Optional
from rest_api_db import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_user_exception, get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .restr import successfull_response, http_exception

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

templetes = Jinja2Templates(directory = "templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Booking(BaseModel):
    name: str = Field(description = "Name of the booking user")
    location: str = Field(description = "Location of the booking user")
    email_id: str = Field(description = "Email id of the booking user")
    phone_number: str = Field(description = "Phone number of the booking user")
    booking_date: str = Field(description = "Enter the date to book the restaurant")
    booking_time: str = Field(description = "Enter the time to book the restaurant")
    complete: bool
    restr_id: int

class BookingCompletion(BaseModel):
    complete: bool

@router.get("/")
async def get_all_booking(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()

@router.post("/")
async def book_restr(booking: Booking, db: Session = Depends(get_db)):
    booking_model = models.Booking()
    booking_model.name = booking.name
    booking_model.location = booking.location
    booking_model.email_id = booking.email_id
    booking_model.phone_number = booking.phone_number
    booking_model.booking_date = booking.booking_date
    booking_model.booking_time = booking.booking_time
    booking_model.complete = False
    booking_model.restr_id = booking.restr_id

    db.add(booking_model)
    db.commit()

    restr_name = db.query(models.Restaurants).filter(models.Restaurants.id == booking.restr_id).first()
    restr_name = restr_name.title

    response = {"name": booking.name, "date" : booking.booking_date, "time" : booking.booking_time, "restr_name": restr_name}
    return successfull_response(201), response

@router.get("/all/{restr_id}")
async def get_booking_by_restr_id(restr_id: int,  db: Session = Depends(get_db)):
    
    # user: dict = Depends(get_current_user),
    # if user is None:
    #     raise get_user_exception()
    
    restr_model = db.query(models.Booking).filter(models.Booking.restr_id == restr_id).all()

    if restr_model is not None:
        return restr_model
    raise http_exception()

@router.get("/pending/{restr_id}")
async def get_pending_booking_by_id(restr_id: int, db: Session = Depends(get_db)):
    restr_model = db.query(models.Booking).filter(models.Booking.restr_id == restr_id).filter(models.Booking.complete == False).all()

    if restr_model is not None:
        return restr_model
    raise http_exception()


@router.put("/{booking_id}")
async def update_booking_by_id(booking_id: int, booking: BookingCompletion, db: Session = Depends(get_db)):

    booking_model = db.query(models.Booking).filter(models.Booking.id == booking_id).first()

    booking_model.complete = booking.complete

    # booking_model.na = booking_model.name
    # booking_model.location = booking_model.location
    # booking_model.email_id = booking_model.email_id
    # booking_model.phone_number = booking_model.phone_number
    # booking_model.booking_date = booking_model.booking_date
    # booking_model.booking_time = booking_model.booking_time
    # booking_model.restr_id = booking_model.restr_id

    db.add(booking_model)
    db.commit()

    return successfull_response(200), {"response": "booking completed"}

@router.delete("/{booking_id}")
async def delete_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    db.query(models.Booking).filter(models.Booking.id == booking_id).delete()

    db.commit()
    
    return successfull_response(200), {"response": "booking deleted"}