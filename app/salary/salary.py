
from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.services.db import get_db



from salary.services.salary import *

salariesRouter = APIRouter()

@salariesRouter.on_event("startup")
async def startup_event():
    create_salaries_from_csv()

templates = Jinja2Templates(directory="salary/templates")

@salariesRouter.get("/salary", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "page": 1, "total_pages": 1})

@salariesRouter.get("/salary/show_from_loc/")
async def show_from_loc(loc: str, db = Depends(get_db)):
    return get_salaries_from_loc(loc, db=db)

@salariesRouter.get("/salary/show_stats_from_loc/")
async def show_stats_from_loc(request: Request, loc: str, db = Depends(get_db)):
    stats =  get_stats_from_loc(loc, db=db)
    salaries = get_salaries_from_loc(loc, db=db)
    return templates.TemplateResponse("stats.html", {"request": request, "stats": stats, "location": loc, "salaries": salaries})

@salariesRouter.get("/salary/show_from_desc/")
async def show_from_desc(request: Request, desc: str, page: int=1, db = Depends(get_db)):
    items_per_page = 20
    offset = (page - 1) * items_per_page
    res, total_pages = search_with_desc(desc, skip=offset, limit=items_per_page, db=db)
    return templates.TemplateResponse("index.html", {"request": request, "salaries": res, "page": page, "total_pages": total_pages})

@salariesRouter.get("/salary/show_cv/")
async def show_cv():
    return show_Mcv()
