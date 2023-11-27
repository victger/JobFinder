from fastapi import APIRouter
from db.services.db import *

import os

dbRouter = APIRouter()

@dbRouter.on_event("startup")
async def startup_event():
    print(os.listdir())
    BaseSQL.metadata.create_all(bind=engine)

