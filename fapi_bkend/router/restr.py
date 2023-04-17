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

# from starlette.responses import JSONResponse
# import uuid
# from random import randint
# from uuid import UUID

# app = FastAPI()
# app.include_router(auth.router)

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

templetes = Jinja2Templates(directory = "templates")




def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Restr(BaseModel):
    title: str = Field(description="Name of the restaurant")
    description: Optional[str] = Field(description="Details of the restaurant")
    category: Optional[str] = Field(description="Cuisine Ex. asian/european")
    sub_category: Optional[str] = Field(description="sub-cuisine Ex. indian/south-indian")
    phone_number: Optional[str] = Field(description="Valid phone number")
    # priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    # complete: bool

@router.get("/test")
async def test(request: Request):
    return templetes.TemplateResponse("home.html", {"request": request})

@router.get("/")
async def read_all(db: Session= Depends(get_db)):
    return db.query(models.Restaurants).all()

# RE-WRITE THE FUNCTION TO RESTR
@router.get("/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Restaurants).filter(models.Restaurants.owner_id == user.get("id")).all()

# RE-WRITE THE FUNCTION TO RESTR
@router.get("/{restr_id}")
async def read_todo(restr_id: int, db: Session = Depends(get_db)):
    #  user: dict = Depends(get_current_user)
    # if user is None:
    #     raise get_user_exception()
    restr_model = db.query(models.Restaurants).filter(models.Restaurants.id == restr_id).first()
    # .filter(models.Restaurants.owner_id == user.get("id"))
    if restr_model is not None:
        return restr_model
    raise http_exception()


@router.post("/")
async def create_restr(restr: Restr, user = 1, db: Session = Depends(get_db)):
    # dict = Depends(get_current_user)
    if user is None:
        raise get_user_exception()
    restr_model = models.Restaurants()
    restr_model.title = restr.title
    restr_model.description = restr.description
    restr_model.category = restr.category
    restr_model.sub_category = restr.sub_category
    restr_model.phone_number = restr.phone_number
    restr_model.owner_id = user
    # restr_model.owner_id = user.get("id)

    db.add(restr_model)
    db.commit()

    response = {"title": restr.title, "description" : restr.description, "category" : restr.category, "sub_category" : restr.sub_category }
    return successfull_response(201), response

# @router.put("/{todo_id}")
# async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
    
#     todo_model = db.query(models.Todos)\
#         .filter(models.Todos.id == todo_id)\
#         .filter(models.Todos.owner_id == user.get("id"))\
#         .first()

#     if todo_model is None:
#         raise http_exception()
    
#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.priority = todo.priority
#     todo_model.complete = todo.complete

#     db.add(todo_model)
#     db.commit()

#     updated_todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
#     return successfull_response(200), updated_todo

# @router.delete("/{todo_id}")
# async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     todo_model_before = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
#     todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()


#     if todo_model is None:
#         raise http_exception()
    
#     db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

#     db.commit()

#     return successfull_response(200), {"message": "Deleted the below todo Succsufullu", "Todo": todo_model_before}

### Below are the reusable functions
def http_exception():
    return HTTPException(status_code=404, detail="Item not found")
    
def successfull_response(status_code: int):
    return {"status": status_code, "transaction": "Successfull."}