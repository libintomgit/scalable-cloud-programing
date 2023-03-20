from fastapi import FastAPI, HTTPException, Request, status, Form, Header, Depends
import models
from todo_db import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from auth import get_user_exception, get_current_user

# from starlette.responses import JSONResponse
# import uuid
from typing import Optional
# from random import randint
# from uuid import UUID

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool
    

@app.get("/todo")
async def read_all(db: Session= Depends(get_db)):
    return db.query(models.Todos).all()

@app.get("/todo/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/todo")
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()
    test = {"title": todo.title, "description" : todo.description, "priority" : todo.priority, "complete" : todo.complete }
    return successfull_response(201), test

@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise http_exception()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    updated_todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    return successfull_response(200), updated_todo

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model_before = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()


    if todo_model is None:
        raise http_exception()
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()

    return successfull_response(200), {"message": "Deleted the below todo Succsufullu", "Todo": todo_model_before}

### Below are the reusable functions
def http_exception():
    return HTTPException(status_code=404, detail="Todo item not found")
    
def successfull_response(status_code: int):
    return {"status": status_code, "transaction": "Successfull."}