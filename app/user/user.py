from fastapi import APIRouter,Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from db.services.db import get_db

from user.services.user import *
from user.models.user import User

userRouter = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="submit_user")
FRONT_PATH = "front/templates/"

async def get_current_user(token: str = Depends(oauth2_scheme), DB: Session = Depends(get_db)):
    user_authenticated = authentication(DB, username=token, password="")
    if user_authenticated:
        return token
    user = DB.query(User).filter(User.name == token).first()
    if user:
        return token
    return None

@userRouter.get("/", response_class=HTMLResponse)
async def read_root():
    with open(f'{FRONT_PATH}/login.html', 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@userRouter.post("/")
async def authenticate(username: str = Form(...), password: str = Form(...),DB: Session = Depends(get_db)):
    if authentication(DB, username, password):
        return RedirectResponse(url="/accueil", status_code=303)
    else:
        with open(f'{FRONT_PATH}/error.html', 'r') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)

@userRouter.get('/create_user')
async def creation():
    with open(f'{FRONT_PATH}/create_user.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)

@userRouter.post('/submit_user')
async def submit_user(
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        return "Username already exists"
    record = create_user(db, name, password)
    return RedirectResponse(url="/accueil", status_code=303)

@userRouter.get('/accueil')
async def accueil():
    with open(f'{FRONT_PATH}/accueil.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)