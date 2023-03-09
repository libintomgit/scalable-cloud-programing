from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from todo_db import SessionLocal, engine
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext

SECRET_KEY = "oNwtaqvwM5KgrgRVRBx4FbMcpL2clcgl"
ALGORITHM = "HS256"



class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(username:str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()
    
@app.get("/users")
async def get_all_users(db: Session= Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name= create_user.first_name
    create_user_model.last_name= create_user.last_name

    hash_passord = get_password_hash(create_user.password)
    create_user_model.hashed_password= hash_passord
    create_user_model.is_active= True

    db.add(create_user_model)
    db.commit()
    full_name = f"{create_user.first_name.title()} {create_user.last_name.title()}"
    return successfull_response(201), {"Username": create_user.username, "Full Name": full_name}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()

    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {"token": token}



### Below are the reusable functions
def successfull_response(status_code: int):
    return {"status": status_code, "transaction": "Successfull."}

# def http_exception(status_code: int):
#     return HTTPException(status_code=status_code, detail="User Not Found.")

def get_user_exception():
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return credentials_exception

def token_exception():
    token_exception_resonse = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    return token_exception_resonse



