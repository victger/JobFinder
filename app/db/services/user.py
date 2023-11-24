from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from schemas import user as SUser
from models import user as MUser


def get_user_by_id(user_id: str, db: Session) -> MUser:
    record = db.query(MUser).filter(MUser.id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def create_user(db: Session, user: SUser.User) -> MUser:
    record = db.query(MUser.User).filter(MUser.id == user.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_post = MUser(**user.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.id = str(db_post.id)
    return db_post