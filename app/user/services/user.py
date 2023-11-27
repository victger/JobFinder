from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime as dt

from user.schemas.user import User as SUser
from user.models.user import User as MUser


def get_user_by_id( db: Session,user_id: str) -> MUser:
    record = db.query(MUser).filter(MUser.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def create_user(db: Session, ids:str, username:str, password:str) -> MUser:
    db_post = MUser(id=ids, username=username, password=password, description="", created_at=dt.now(), updated_at=dt.now())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.id = str(db_post.id)
    return db_post

def authentication(db: Session, username:str, password:str) -> bool:
    record = db.query(MUser).filter(MUser.name == username and MUser.password == password).first()
    if not record:
        return False
    return True