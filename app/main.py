from sqlalchemy.orm import Session

from datetime import timedelta

from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse


from db.db import dbRouter

from salary.salary import salariesRouter

from user.user import userRouter

from jobs.jobs import jobsRouter

from jobs.services.jobs import create_bucket

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

### MINIO ###

### BACK END

app.include_router(dbRouter)

app.include_router(salariesRouter)

app.include_router(userRouter)

app.include_router(jobsRouter)