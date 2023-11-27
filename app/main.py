from sqlalchemy.orm import Session

from datetime import timedelta
from minio import Minio

from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse

from db.services.user import *
from db.models.db import BaseSQL, engine, get_db
from db.models.user import User 

from db.models.salary import Salary

from typing import Optional, List

import pandas as pd
import numpy as np
import os

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)


### POSTGRE SQL

@app.on_event("startup")
async def startup_event():
    csv_file_path = "data/salaries.csv"
    BaseSQL.metadata.create_all(bind=engine)
    df = pd.read_csv(csv_file_path)
    df["id"] = np.arange(len(df))
    print("result----------------------", df.index)
    df.to_sql("salaries", engine, if_exists="replace", index=False)


@app.get("/", response_class=HTMLResponse)
def read_root():
    file_path = 'front/templates/accueil_content.html'
    with open(file_path, 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@app.post("/")
def authenticate(username: str = Form(...), password: str = Form(...)):
    if authentication(get_db(), username, password):
        return "OKAY BG"
    else:
        error_message = "Incorrect password"
        file_path = 'front/templates/error.html'
        with open(file_path, 'r') as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)

@app.get("/salaries/")
def get_salaries(skip: int = 0, limit: int = 1, db = Depends(get_db)):
    query = db.query(Salary).offset(skip).limit(limit)
    res = query.all()
    return res

### USER ###    

@app.get('/create_user')
async def creation():
    with open('front/templates/create_user.html', 'r') as file:
        html_content = file.read()
    return HTMLResponse(content= html_content, status_code=200)

@app.post('/submit_user')
async def submit_user(ids:str = Form(...),name: str = Form(...), password: str = Form(...)):
    create_user(get_db(), ids, name, password)
    return "OKAY BG"


### MINIO ###

client = Minio("minio:9000", "root", "rootpassword", secure=False)

@app.get('/bucket/show/')
async def show_bucket():
    buckets = client.list_buckets()
    return {'result': buckets}
