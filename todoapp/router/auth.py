import sys
sys.path.append("..")

from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from todo_db import SessionLocal, engine
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

SECRET_KEY = "oNwtaqvwM5KgrgRVRBx4FbMcpL2clcgl"
ALGORITHM = "HS256"



class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    phone_number: Optional[str]
    password: str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

templetes = Jinja2Templates(directory = "templates")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# app = FastAPI()
router = APIRouter(prefix="/api/auth", tags=["auth"], responses={401: {"user": "Not Authorised"}})

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.passwrod = form.get("password")

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

def authenticate_user(username:str, password: str, db: Session = Depends(get_db)):
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

async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise None
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()
    
@router.get("/users")
async def get_all_users(db: Session= Depends(get_db)):
    return db.query(models.Users).all()

@router.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name= create_user.first_name
    create_user_model.last_name= create_user.last_name
    create_user_model.phone_number = create_user.phone_number

    hash_passord = get_password_hash(create_user.password)
    create_user_model.hashed_password= hash_passord
    create_user_model.is_active= True

    db.add(create_user_model)
    db.commit()
    full_name = f"{create_user.first_name.title()} {create_user.last_name.title()}"
    return successfull_response(201), {"Username": create_user.username, "Full Name": full_name}

@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False

    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)
    return True

@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templetes.TemplateResponse("login.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/api/todo", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token (response=response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templetes.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknow error"
        return templetes.TemplateResponse("login.html", {"request": request, "msg": msg})

@router.get("/register", response_class=HTMLResponse)
async def user_registration_page(request: Request):
    return templetes.TemplateResponse("register.html", {"request": request})

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



