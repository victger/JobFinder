from sqlalchemy.orm import Session
from datetime import datetime as dt

from uuid import uuid4

from user.schemas.user import User as SUser
from user.models.user import User as MUser

def get_user(db: Session,user_id: str) -> MUser:
    record = db.query(MUser).filter(MUser.id == user_id).first()
    if not record:
        return None
    return record

def create_user(db: Session, username:str, password:str):
    db_post = MUser(id=uuid4(), name=username, password=password, created_at=str(dt.now()))
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def authentication(db: Session, username:str, password:str) -> bool:
    record = db.query(MUser).filter(MUser.name == username and MUser.password == password).first()
    return record!=None