from sqlalchemy.orm import Session
from datetime import timedelta
from minio import Minio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from db.services.user import authentication
from db.models.db import BaseSQL, engine, DB 

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
    file_path = 'front/templates/index.html'
    with open(file_path, 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@app.post("/authenticate")
def authenticate(username: str = Form(...),password: str = Form(...)):
    if authentication(DB,username, password):
        return "OKAY BG"
    else:
        return "NOT OKAY BG"

'''@app.get('/error', response_class=HTMLResponse)
def error():
    file_path = 'front/templates/index.html'
    with open(file_path, 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)'''