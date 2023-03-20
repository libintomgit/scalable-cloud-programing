from fastapi import FastAPI, Depends
from todo_db import engine
from router import auth, todos, users, address
import models
from company import companyapis, dependecies
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router, prefix="/api/companyapis", tags=["companyapis"], dependencies=[Depends(dependecies.get_token_header)], responses={418: {"description": "Internal user only"}})
app.include_router(users.router)
app.include_router(address.router)