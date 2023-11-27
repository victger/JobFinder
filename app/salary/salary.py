
from fastapi import Depends, APIRouter

from db.services.db import get_db

from salary.models.salary import Salary
from salary.services.salary import *

salariesRouter = APIRouter()

@salariesRouter.on_event("startup")
async def startup_event():
    create_salaries_from_csv()

@salariesRouter.get("/salaries/show")
def show_salaries(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    res = get_salaries(skip, limit, db)
    return res