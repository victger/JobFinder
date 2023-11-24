from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .db import BaseSQL


class User(BaseSQL):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    description = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())