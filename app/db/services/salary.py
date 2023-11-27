import pandas as pd
import numpy as np

from fastapi import Depends
from db.models.db import engine, get_db


def create_salaries_from_csv(csv_path: str="data/salaries.csv"):
    df = pd.read_csv(csv_path)
    df["id"] = np.arange(len(df))
    df.to_sql("salaries", engine, if_exists="replace", index=False)