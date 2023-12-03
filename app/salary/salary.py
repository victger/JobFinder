
from fastapi import Depends, APIRouter, Request, File, UploadFile, Cookie

from fastapi.templating import Jinja2Templates

from db.services.db import get_db

from salary.services.salary import *

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from user.user import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction de validation du token
# def get_current_user(token_cookie: str = Cookie(...)):
#     # Vous pouvez ici vérifier la validité du token
#     print("_" * 20)
    
#     if not (isinstance(token_cookie, str) and len(token_cookie) > 0):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     # Ajoutez ici la logique de validation de votre token si nécessaire

#     return token_cookie

salariesRouter = APIRouter()

@salariesRouter.on_event("startup")
async def startup_event():
    create_salaries_from_csv()

templates = Jinja2Templates(directory="salary/templates")

@salariesRouter.get("/salary/", dependencies=[Depends(get_current_user)])
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "page": 1, "total_pages": 1, "loc": "US", "desc": "Data"})


@salariesRouter.get("/salary/show_salaries/")
async def show_from_desc(request: Request, loc: str, desc: str, page: int=1, db = Depends(get_db)):
    items_per_page = 20
    offset = (page - 1) * items_per_page
    res, stats, total_pages = search_salaries(loc, desc, skip=offset, limit=items_per_page, db=db)
    return templates.TemplateResponse("index.html", {"request": request, "salaries": res, "page": page, "total_pages": total_pages, "loc":loc, "desc": desc, 'stats': stats})

@salariesRouter.get("/salary/show_cv/")
async def show_cv(request: Request):
    return show_Mcv(request.cookies["token"])

@salariesRouter.post("/salary/add_cv/")
async def add_cv(request: Request, file: UploadFile = File(...)):
    add_Mcv(request.cookies["token"], file)
    return {"message": "CV ajouté avec succès"}

