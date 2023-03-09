from fastapi import FastAPI, Depends
from todo_db import engine
from router import auth, todos, users
import models
from company import companyapis, dependecies


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router, prefix="/api/companyapis", tags=["companyapis"], dependencies=[Depends(dependecies.get_token_header)], responses={418: {"description": "Internal user only"}})
app.include_router(users.router)