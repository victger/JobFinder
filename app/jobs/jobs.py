
from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.services.db import get_db
from jobs.services.jobs import *
from Minio.minio import client

import os

jobsRouter = APIRouter()

FOLDER_PATH= "data/fiche_metier"

@jobsRouter.on_event("startup")
async def startup_event(bucket_name: str="jobs-pdf", folder_path: str=FOLDER_PATH, client= client):
    create_bucket(client, bucket_name)
    put_pdf_bucket(client, bucket_name, folder_path)

@jobsRouter.get('/jobs', response_class=HTMLResponse)
async def show_jobs(request : Request):
    return templates.TemplateResponse('index.html', {"request": request})

templates = Jinja2Templates(directory="jobs/templates")


