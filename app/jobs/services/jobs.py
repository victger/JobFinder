import pandas as pd
import numpy as np
import os
from datetime import timedelta

from sqlalchemy import func

from fastapi import Depends
from salary.models.salary import Salary
from db.services.db import engine, get_db
from Minio.minio import client


def jobs_list():

    csv_file = 'data/salaries.csv'
    df = pd.read_csv(csv_file)
    jobs = df['job_title'].unique().tolist()

    return jobs

def create_bucket(client, bucket_name: str):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

def put_pdf_bucket(client, bucket_name: str, folder_path: str):
    files = os.listdir(folder_path)
    for file_name in files:
        object_name = file_name
        file_path = os.path.join(folder_path, file_name)
        try:
            client.fget_object(bucket_name, object_name)
        except Exception as e:
            try:
                client.fput_object(bucket_name, object_name, file_path)
            except Exception as e:
                pass

def generate_download_url(client= client):
    try:
        return client.presigned_get_object("jobs-pdf", "Data Scientist.pdf")
    except Exception as e:
        print(f"Erreur lors de la génération de l'URL signée : {str(e)}")
        return None