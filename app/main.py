from datetime import datetime, date
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated
from typing import Optional

from minio import Minio
from fastapi import FastAPI, File, UploadFile

from datetime import timedelta

from db.models.db import BaseSQL, engine


app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

client = Minio("minio:9000", "root", "rootpassword", secure=False)



@app.post('/file/upload/')
async def upload_file(file: UploadFile = File(...)):
    result = client.put_object("name", file.filename, file.file, 5000)
    return {'result': result}



@app.put('/file/presigned/')
async def put_presigned_file(name: str):
    put_url  = client.get_presigned_url(
        "GET",
        "name",
        name,
        expires=timedelta(days=1),
        response_headers={"response-content-type": "application/json"},
    )
    return put_url

@app.get('/file/presigned/')
async def get_presigned_file(name: str):
    put_url  = client.get_presigned_url(
        "GET",
        "name",
        name,
        expires=timedelta(days=1),
        response_headers={"response-content-type": "application/json"},
    )
    return put_url

@app.get('/bucket/show/')
async def show_bucket(name: str):
    objects = client.list_objects(name, recursive=True)
    return {'result': '\n'.join([object.object_name for object in objects])}


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)
