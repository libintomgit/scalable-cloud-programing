from fastapi import FastAPI, Depends
from rest_api_db import engine
from router import auth, restr, users, address, booking
import models
from company import companyapis, dependecies
from starlette.staticfiles import StaticFiles
from http import HTTPStatus

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return {"status": HTTPStatus.OK, "transaction": "Successfull."}

app.include_router(auth.router, prefix="/api/auth", tags=["auth"], responses={401: {"user": "Not Authorised"}})
app.include_router(restr.router, prefix="/api/restr", tags=["restr"], responses={401: {"user": "Not Authorised"}})
app.include_router(users.router, prefix="/api/users", tags=["users"], responses={404: {"description": "User not found."}})
app.include_router(address.router, prefix="/api/address", tags=["address"], responses={404: {"description": "Not found"}})
app.include_router(booking.router, prefix="/api/booking", tags=["booking"], responses={404: {"description": "Not found"}})

# COMMENT HERE
# app.include_router(companyapis.router, prefix="/api/companyapis", tags=["companyapis"], dependencies=[Depends(dependecies.get_token_header)], responses={418: {"description": "Internal user only"}})