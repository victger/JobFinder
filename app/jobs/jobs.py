from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from jobs.services.jobs import *

jobsRouter = APIRouter()
templates = Jinja2Templates(directory="jobs/templates")

FOLDER_PATH= "data/fiche_metier"

@jobsRouter.on_event("startup")
async def startup_event(bucket_name: str="jobs-txt", folder_path: str=FOLDER_PATH, client= client):
    create_bucket(client, bucket_name)
    put_pdf_bucket(client, bucket_name, folder_path)

@jobsRouter.get('/jobs', response_class=HTMLResponse)
async def show_jobs(request : Request):
    jobs= jobs_list()
    return templates.TemplateResponse('index.html', {"request": request, "jobs": jobs})

@jobsRouter.get("/jobs/download/{job}")
async def download_info_endpoint(request : Request, job):
    download_object(job)
    return templates.TemplateResponse('download.html', {"request": request})