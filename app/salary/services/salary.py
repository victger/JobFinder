import pandas as pd
import numpy as np

from sqlalchemy import func

from fastapi import Depends
from salary.models.salary import Salary

from db.services.db import engine, get_db
from Minio.minio import client

from io import BytesIO
import PyPDF2
SALARY_PATH = "data/salaries.csv"



def create_salaries_from_csv(csv_path: str=SALARY_PATH):
    df = pd.read_csv(csv_path)
    df["id"] = np.arange(len(df))
    df.to_sql("salaries", engine, if_exists="replace", index=False)

def get_salaries(skip=1, limit=10, db = Depends(get_db)):
    res = db.query(Salary).offset(skip).limit(limit).all()
    return res

def get_salaries_from_loc(loc: str, skip=1, limit=10, db=Depends(get_db)):
    return db.query(Salary).filter(Salary.company_location.ilike(loc)).offset(skip).limit(limit).all()

def get_mean_salary(query):
    return query.session.query(func.avg(Salary.salary)).scalar()

def get_stats_from_loc(loc: str, db: Depends(get_db)=Depends(get_db)):
    mean = db.query(func.avg(Salary.salary)).filter(Salary.company_location.ilike(loc)).scalar()
    mean = round(mean)
    size = db.query(Salary).count()
    return mean, size

def get_mean_salary(df):
    pass

def show_linkedIn():
    pass

def search_with_desc(desc: str, skip=1, limit=10, db=Depends(get_db)):
    res = db.query(Salary).filter(Salary.job_title.ilike(desc))
    total_pages = res.count() // limit + 1
    res = res.offset(skip).limit(limit).all()
    return res, total_pages

def show_Mcv():
    pdf_data  = client.get_object(
        "users",
        "test/Stage 6 mois AIRBUS.pdf",
    ).read()
    pdf_document = PyPDF2.PdfReader(BytesIO(pdf_data))
    text = ""
    for page_num in range(len(pdf_document.pages)):
            page = pdf_document.pages[page_num]
            text += page.extract_text()
    return {"text": text}

