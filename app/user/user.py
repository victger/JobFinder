from fastapi import APIRouter,Form, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from user.services.user import *
from db.services.db import get_db
from datetime import timedelta, datetime as dt
from jose import jwt,JWTError
import hashlib

userRouter = APIRouter()
FRONT_PATH = "front/templates/"
SECRET_KEY = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = dt.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def auth_token(db: Session, token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id:
            return get_user_token(db,token) is not None
    except JWTError:
        pass
    return False

async def get_current_user(request: Request, DB: Session = Depends(get_db)):
    try:
        token = request.headers.get("cookie", "")[6:]
        user_authenticated = auth_token(DB, token)
        if user_authenticated:
            return token
    except:
        pass
    return RedirectResponse(url="/", status_code=303)

def login(DB: Session,record):
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(record.id)}, expires_delta=token_expires)
    record.token = access_token
    response = RedirectResponse(url="/accueil", status_code=303)
    response.set_cookie(key="token", value=access_token, expires=timedelta(hours=1), secure=False, httponly=True)
    DB.commit()
    return response

@userRouter.get("/", response_class=HTMLResponse)
async def read_root():
    with open(f'{FRONT_PATH}/login.html', 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@userRouter.post("/")
async def split_accueil(username: str = Form(...), password: str = Form(...),DB: Session = Depends(get_db)):
    hashed = hashlib.sha256(password.encode())
    record = authenticate_user(DB, str(username), str(hashed.hexdigest()))
    if record is not None:
        return login(DB, record)
    else:
        with open(f'{FRONT_PATH}/login.html', 'r') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content.replace('Hello please login for your favorite content !','Your username or password may be incorrect'), status_code=200)

@userRouter.get('/create_user')
async def creation():
    with open(f'{FRONT_PATH}/create_user.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)

@userRouter.post('/create_user')
async def submit_user(username: str = Form(...),password: str = Form(...),db: Session = Depends(get_db)):
    if len(username) < 4 or len(password) < 4:
        with open(f'{FRONT_PATH}/create_user.html', 'r') as file:
            html_content = file.read()
            return HTMLResponse(content= html_content.replace('Please create an account','Username or password too short, please change to have more than 4 characters for each'), status_code=200)
        
    if get_user(db, username) is not None:
            with open(f'{FRONT_PATH}/create_user.html', 'r') as file:
                html_content = file.read()
                return HTMLResponse(content= html_content.replace('Please create an account','Username already taken, please change'), status_code=200)
    hashed = hashlib.sha256(password.encode())
    record = create_user(db, str(username), str(hashed.hexdigest()))
    return login(db, record)

@userRouter.get('/accueil')
async def accueil(request: Request, user_token = Depends(get_current_user),DB: Session = Depends(get_db)):
    if type(user_token) is not str:
        return user_token
    
    with open(f'{FRONT_PATH}/accueil.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content.replace('user',get_user_token(DB,user_token).username), status_code=200)
