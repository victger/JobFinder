
from fastapi import Depends, APIRouter

from db.services.db import get_db



from salary.models.salary import Salary
from salary.services.salary import *

salariesRouter = APIRouter()

@salariesRouter.on_event("startup")
async def startup_event():
    create_salaries_from_csv()

@salariesRouter.get("/salary/show")
def show_salaries(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    return get_salaries(skip, limit, db)

@salariesRouter.get("/salary/show_from_loc/")
def show_from_loc(loc: str, db = Depends(get_db)):
    return get_salaries_from_loc(loc, db=db)

@salariesRouter.get("/salary/stats_from_loc/")
def show_from_loc(loc: str, db = Depends(get_db)):
    return get_stats_from_loc(loc, db=db)
