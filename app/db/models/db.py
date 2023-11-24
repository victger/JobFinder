from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
<<<<<<< HEAD
import os
=======
from dotenv import load_dotenv

import os 

dotenv_path = os.path.join(os.path.dirname(__file__), "../../../.env")  # Ajustez le chemin en fonction de votre structure de répertoire
load_dotenv(dotenv_path)
>>>>>>> d670075dc782fbee2a47398b2f6c4626ccf91b60

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = "db"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

BaseSQL = declarative_base()