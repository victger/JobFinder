from fastapi import APIRouter,Form, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from user.services.user import *
from db.services.db import get_db
from user.models.user import User
from datetime import timedelta, datetime as dt
from jose import jwt,JWTError

userRouter = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="submit_user")
FRONT_PATH = "front/templates/"
SECRET_KEY = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
            return db.query(User).filter(User.id == user_id, User.token == token).first() is not None
    except JWTError:
        return False
    return False

async def get_current_user(token: str = Depends(oauth2_scheme), DB: Session = Depends(get_db)):
    user_authenticated = auth_token(DB, token)
    if user_authenticated:
        return token
    user = DB.query(User).filter(User.token == token).first()
    if user:
        return token
    return None

@userRouter.get("/", response_class=HTMLResponse)
async def read_root():
    with open(f'{FRONT_PATH}/login.html', 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@userRouter.post("/")
async def authenticate(username: str = Form(...), password: str = Form(...),DB: Session = Depends(get_db)):
    user = authenticate_user(DB, username, password)
    if user:
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.id}, expires_delta=token_expires)
        user.token = access_token
        DB.commit()
        return RedirectResponse(url="/accueil", status_code=303, headers={"Authorization": f"Bearer {access_token}"})
    else:
        with open(f'{FRONT_PATH}/error.html', 'r') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)

@userRouter.get('/create_user')
async def creation():
    with open(f'{FRONT_PATH}/create_user.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)

@userRouter.post('/submit_user')
async def submit_user(
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        return "Username already exists, please put another name"
    record = create_user(db, name, password)
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": record.id}, expires_delta=token_expires)
    record.token = access_token
    db.commit()
    return RedirectResponse(url="/accueil", status_code=303, headers={"Authorization": f"Bearer {access_token}"})

@userRouter.get('/accueil')
async def accueil(user = Depends(get_current_user)):
    with open(f'{FRONT_PATH}/accueil.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)