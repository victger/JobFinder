
from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.services.db import get_db



from salary.models.salary import Salary
from salary.services.salary import *

import os

salariesRouter = APIRouter()

@salariesRouter.on_event("startup")
async def startup_event():
    create_salaries_from_csv()

templates = Jinja2Templates(directory="salary/templates")

@salariesRouter.get("/salary", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@salariesRouter.get("/salary/show")
def show_salaries(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    return get_salaries(skip, limit, db)

@salariesRouter.get("/salary/show_from_loc/")
def show_from_loc(loc: str, db = Depends(get_db)):
    return get_salaries_from_loc(loc, db=db)

@salariesRouter.get("/salary/show_stats_from_loc/")
def show_stats_from_loc(request: Request, loc: str, db = Depends(get_db)):
    stats =  get_stats_from_loc(loc, db=db)
    salaries = get_salaries_from_loc(loc, db=db)
    return templates.TemplateResponse("stats.html", {"request": request, "stats": stats, "location": loc, "salaries": salaries})
