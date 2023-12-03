from sqlalchemy.orm import Session
from datetime import datetime as dt
from uuid import uuid4
from user.models.user import User as MUser
from datetime import timedelta, datetime as dt
from fastapi import APIRouter,Form, Depends, Request
from db.services.db import get_db
from jose import jwt,JWTError
from fastapi.responses import HTMLResponse, RedirectResponse

FRONT_PATH = "front/templates/"
SECRET_KEY = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def login(DB: Session,record):
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(record.id)}, expires_delta=token_expires)
    record.token = access_token
    response = RedirectResponse(url="/accueil", status_code=303)
    response.set_cookie(key="token", value=access_token, expires=timedelta(hours=1), secure=False, httponly=True)
    DB.commit()
    return response

def get_user(db: Session,username: str) -> MUser:
    record = db.query(MUser).filter(MUser.username == username).first()
    if not record:
        return None
    return record

def create_user(db: Session, username:str, password:str):
    db_post = MUser(id=uuid4(), username=username, password=password, created_at=str(dt.now()))
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def authenticate_user(db: Session, username: str, password: str):
    record = db.query(MUser).filter(MUser.username == username, MUser.password == password).first()
    return record

def get_user_token(db: Session, token: str):
    record = db.query(MUser).filter(MUser.token == token).first()
    return record

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

def get_current_user(request: Request, DB: Session = Depends(get_db)):
    try:
        token = request.cookies["token"]
        user_authenticated = auth_token(DB, token)
        if user_authenticated:
            print("token: ", token)
            return token
    except:
        pass
    return RedirectResponse(url="/", status_code=303)
