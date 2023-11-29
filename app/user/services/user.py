from sqlalchemy.orm import Session
from datetime import datetime as dt
from uuid import uuid4
from user.models.user import User as MUser

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