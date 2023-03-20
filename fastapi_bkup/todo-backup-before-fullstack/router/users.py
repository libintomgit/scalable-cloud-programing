import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
import models
from todo_db import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception, verify_password, get_password_hash

router = APIRouter(prefix="/api/users", tags=["users"], responses={404: {"description": "User not found."}})

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class UserVerification(BaseModel):
    username: str
    pasword: str
    new_password: str

@router.get("/")
async def reall_all_user(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.get("/{user_id}")
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"

@router.get("/user/")
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User ID"

@router.put("/user/password")
async def user_password_change(user_verification: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(user_verification.pasword, user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "Successfully updated the password!"
    return "Invalid user or request"

# @router.put("/update/user")
# async def user_details_update(user_)

@router.delete("/user")
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        return "Invalid user or request"

    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    db.commit()

    return {"username": user_model.username, "Message": "User deleted successfully!"}