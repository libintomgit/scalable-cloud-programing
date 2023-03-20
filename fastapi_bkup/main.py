# import uvicorn
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field
import uuid
from typing import Optional
from random import randint
from uuid import UUID

class NegativeNumberException(Exception):
    def __init__(self, restr_to_return):
        self.restr_to_return = restr_to_return


app = FastAPI()

class Restr(BaseModel):
    id: UUID
    name: str = Field(title="Enter the name of the restaurant", min_length=4, max_length=20)     
    short_description: str = Field(title="Short description about the restaurant", max_length=30, min_length=10)
    long_description: Optional[str] = Field(title="Long description about the restaurant", max_length=100, min_length=10)
    location: str = Field(title="Enter the location details", max_length=100, min_length=5)
    phone_number: int 
    email_id: str
    rating: int = Field(title="Raiting between 0 to 100", gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": f"{uuid.uuid4()}",
                 "name" : f"restaurant_name",
                "short_description" : "stringstri",
                "long_description" : "stringstri",
                "location" : "example location",
                "phone_number" : "123456789",
                "email_id" : "example@example.com",
                "rating" : 55
            }
        }

class RestrNoRating(BaseModel):
    id: UUID
    name: str = Field(title="Enter the name of the restaurant", min_length=4, max_length=20)     
    short_description: str = Field(title="Short description about the restaurant", max_length=30, min_length=10)
    long_description: Optional[str] = Field(title="Long description about the restaurant", max_length=100, min_length=10)
    location: str = Field(title="Enter the location details", max_length=100, min_length=5)
    phone_number: int 
    email_id: str


restr_list = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message": f"You are searching for {exception.restr_to_return} restaurant!"})

@app.get("/api/restr/")
async def read_all_restr(restr_to_return: Optional[int] = None):
    if len(restr_list) < 1:
        create_restr_no_api()
    
    if restr_to_return and restr_to_return < 0:
        raise NegativeNumberException(restr_to_return=restr_to_return)

    if restr_to_return and len(restr_list) >= restr_to_return > 0:
        i = 1
        new_restr = []
        while i <= restr_to_return:
            new_restr.append(restr_list[i - 1])
            i += 1
        return new_restr
    return restr_list

@app.get("/api/restr/rating/{restr_id}", response_model=RestrNoRating)
async def read_restr_no_rating(restr_id: UUID):
    for x in restr_list:
        if x.id == restr_id:
            return x
    raise raise_item_cannot_found_exception()

@app.get("/api/restr/id/{restr_id}")
async def read_restr(restr_id: UUID):
    for x in restr_list:
        if x.id == restr_id:
            return x
    raise raise_item_cannot_found_exception()

def create_restr_no_api():
    num = 5
    for i in range(num):
        restr_add = Restr(  id = f"{uuid.uuid4()}",
                            name = f"restaurant_{i+1}",
                            short_description = "stringstri",
                            long_description = "stringstri",
                            location = "example location",
                            phone_number = 123456789,
                            email_id = f"example_{i+1}@example.com",
                            rating = 55+i)

        restr_list.append(restr_add)


@app.post("/api/restr/", status_code=status.HTTP_201_CREATED)
async def create_restr(restr:Restr):
    restr_list.append(restr)
    return restr_list


@app.put("/api/restr/id/{restr_id}")
async def update_restr(rest_id: UUID, restrs: Restr):
    counter = 0
    for x in restr_list:
        counter += 1
        if x.id == rest_id:
            restr_list[counter - 1] = restrs
            return restr_list[counter - 1]
    raise raise_item_cannot_found_exception()


@app.delete("/api/restr/id/{restr_id}")
async def delete_restr(restr_id: UUID):
    counter = 0
    for x in restr_list:
        counter += 1
        if x.id == restr_id:
            del restr_list[counter - 1]
            return f"ID: {restr_id} has been deleted successfully"
    raise raise_item_cannot_found_exception()

def raise_item_cannot_found_exception():
    return HTTPException(status_code=404, detail="Restaurant id not found", headers={"X-Header-Error": "Could not find Restaurant with the provided UUID"})

@app.post("/api/restr/login/")
async def restr_login(restr_id:int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == 'FastAPIUser' and password == 'test1234':
        return restr_list[restr_id]
    return {"username": username, "password": password, "message": "Is Invalid"}


@app.get("/api/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


