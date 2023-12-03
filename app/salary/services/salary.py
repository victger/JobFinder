import pandas as pd
import numpy as np
import io
from sqlalchemy import func

from fastapi import Depends, UploadFile, Query
from salary.models.salary import Salary

from db.services.db import engine, get_db
from Minio.minio import client

from io import BytesIO
import PyPDF2
from tkinter import Tk, filedialog

from Minio.minio import client
SALARY_PATH = "data/salaries.csv"



def create_salaries_from_csv(csv_path: str=SALARY_PATH):
    df = pd.read_csv(csv_path)
    df["id"] = np.arange(len(df))
    df.to_sql("salaries", engine, if_exists="replace", index=False)

def get_mean_salary(query):
    return query.session.query(func.avg(Salary.salary)).scalar()

def get_stats_from_loc(loc: str, db: Depends(get_db)=Depends(get_db)):
    mean = db.query(func.avg(Salary.salary)).filter(Salary.company_location.ilike(loc)).scalar()
    mean = round(mean)
    size = db.query(Salary).count()
    return mean, size

def get_mean_salary(df):
    pass

def search_with_loc_and_desc(query: Query, loc: str = None, desc: str = None):
    if loc:
        print(loc)
        query = query.filter(func.lower(Salary.company_location).like(func.lower(f"%{loc}%")))
    if desc:
        query = query.filter(func.lower(Salary.job_title).like(func.lower(f"%{desc}%")))
    return query

def get_page(query: Query, skip=1, limit=10, ):
    return query.offset(skip).limit(limit).all()

def search_salaries(loc: str, desc: str, skip=1, limit=10, db=Depends(get_db)):
    query = db.query(Salary)
    query = search_with_loc_and_desc(query, loc, desc)
    tot = query.count()
    query = query.offset(skip).limit(limit)
    page = query.all()
    total_pages = tot // limit + 1
    stats = None
    return page, stats, total_pages

def show_Mcv(user_token: str):
    pdf_data  = client.get_object(
        "users",
        f"{user_token}/cv.pdf",
    ).read()
    pdf_document = PyPDF2.PdfReader(BytesIO(pdf_data))
    text = ""
    for page_num in range(len(pdf_document.pages)):
            page = pdf_document.pages[page_num]
            text += page.extract_text()
    return {"text": text}

def add_Mcv(user_token: str, file: UploadFile):
    content = file.file.read()
    content_stream = io.BytesIO(content)
    client.put_object("users", f"{user_token}/cv.pdf", content_stream, len(content))
    return None