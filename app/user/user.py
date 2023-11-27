
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile, Form, Depends

from db.services.db import get_db

from user.services.user import *

userRouter = APIRouter()

FRONT_PATH = "front/templates/"

### USER ###    

@userRouter.get('/create_user')
async def creation():
    with open(f'{FRONT_PATH}/create_user.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)

@userRouter.post('/submit_user')
async def submit_user(ids:str = Form(...),name: str = Form(...), password: str = Form(...)):
    create_user(get_db(), ids, name, password)
    return "OKAY BG"

@userRouter.get("/", response_class=HTMLResponse)
def read_root():
    with open(f'{FRONT_PATH}/accueil_content.html', 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@userRouter.post("/")
def authenticate(username: str = Form(...), password: str = Form(...)):
    if authentication(get_db(), username, password):
        return "OKAY BG"
    else:
        error_message = "Incorrect password"
        with open(f'{FRONT_PATH}/error.html', 'r') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)

