from sqlalchemy.orm import Session
from datetime import timedelta
from minio import Minio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from db.services.user import *
from db.models.db import BaseSQL, engine, DB
from db.models.user import User 
from typing import Optional

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

client = Minio("minio:9000", "root", "rootpassword", secure=False)

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

@app.get('/bucket/show/')
async def show_bucket(name: str):
    objects = client.list_objects(name, recursive=True)
    return {'result': '\n'.join([object.object_name for object in objects])}

@app.get("/", response_class=HTMLResponse)
def read_root():
    file_path = 'front/templates/accueil_content.html'
    with open(file_path, 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@app.post("/")
def authenticate(username: str = Form(...), password: str = Form(...)):
    if authentication(DB, username, password):
        return "OKAY BG"
    else:
        error_message = "Incorrect password"
        file_path = 'front/templates/error.html'
        with open(file_path, 'r') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)
        
@app.get('/create_user')
async def creation():
    with open('front/templates/create_user.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)

@app.post('/submit_user')
async def submit_user(ids:str = Form(...),name: str = Form(...), password: str = Form(...)):
    create_user(DB, ids, name, password)
    return "OKAY BG"