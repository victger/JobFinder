import pandas as pd
import os

from fastapi import Depends
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

def generate_download_url(job: str):
    try:
        file_info = client.fget_object("jobs-txt", f"{job}.txt", "temporary-file-path")
        if file_info:
            return client.presigned_get_object("jobs-txt", f"{job}.txt")
        else:
            print(f"Le fichier {job}.txt n'existe pas dans le bucket 'jobs-txt'.")
            return None
    except Exception as e:
        print(f"Erreur lors de la génération de l'URL signée : {str(e)}")
        return None