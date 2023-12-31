from dotenv import load_dotenv

import os 

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")  # Ajustez le chemin en fonction de votre structure de répertoire
load_dotenv(dotenv_path)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = "db"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"
print(SQLALCHEMY_DATABASE_URL)
