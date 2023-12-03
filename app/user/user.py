from fastapi import APIRouter,Form, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from user.services.user import *
from db.services.db import get_db
from datetime import timedelta, datetime as dt
from jose import jwt,JWTError
import hashlib

userRouter = APIRouter()


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
    return HTMLResponse(content = html_content.replace('user',get_user_token(DB,user_token).username), status_code=200)
