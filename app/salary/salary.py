
from fastapi import Depends, APIRouter, Request, File, UploadFile

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.services.db import get_db

from user.services.user import get_current_user

from salary.services.salary import *

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction de validation du token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Vous pouvez ici vérifier la validité du token
    print("token type", type(token))
    print("_"*20)
    if type(token) is not str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

salariesRouter = APIRouter()

@salariesRouter.on_event("startup")
async def startup_event():
    create_salaries_from_csv()

templates = Jinja2Templates(directory="salary/templates")

@salariesRouter.get("/salary", response_class=HTMLResponse)
async def show_form(request: Request):
    print(request.cookies)
    return templates.TemplateResponse("index.html", {"request": request, "page": 1, "total_pages": 1, "loc": "US", "desc": "Data"})


@salariesRouter.get("/salary/show_salaries/")
async def show_from_desc(request: Request, loc: str, desc: str, page: int=1, db = Depends(get_db)):
    items_per_page = 20
    offset = (page - 1) * items_per_page
    res, stats, total_pages = search_salaries(loc, desc, skip=offset, limit=items_per_page, db=db)
    return templates.TemplateResponse("index.html", {"request": request, "salaries": res, "page": page, "total_pages": total_pages, "loc":loc, "desc": desc})

@salariesRouter.get("/salary/show_cv/")
async def show_cv(request: Request):
    return show_Mcv(request.cookies["token"])

@salariesRouter.post("/salary/add_cv/")
async def add_cv(request: Request, file: UploadFile = File(...)):
    add_Mcv(request.cookies["token"], file)
    return {"message": "CV ajouté avec succès"}

