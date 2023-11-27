from sqlalchemy.orm import Session

from datetime import timedelta
from minio import Minio

from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse


from db.db import dbRouter

from salary.salary import salariesRouter

from user.user import userRouter


app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

### MINIO ###

client = Minio("minio:9000", "root", "rootpassword", secure=False)

@app.get('/bucket/show/')
async def show_bucket():
    buckets = client.list_buckets()
    return {'result': buckets}


### POSTGRE SQL
app.include_router(dbRouter)

app.include_router(salariesRouter)

app.include_router(userRouter)

### FRONT


