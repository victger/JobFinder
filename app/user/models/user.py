from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.services.db import BaseSQL


class User(BaseSQL):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    token = Column(String)
    created_at = Column(String)