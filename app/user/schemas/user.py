from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class User(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    username: str
    password: str
    token: str = ""
    created_at: str