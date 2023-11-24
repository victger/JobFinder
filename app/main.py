from datetime import timedelta
from minio import Minio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from db.services.user import authentication

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

client = Minio("minio:9000", "root", "rootpassword", secure=False)

@app.get('/bucket/show/')
async def show_bucket(name: str):
    objects = client.list_objects(name, recursive=True)
    return {'result': '\n'.join([object.object_name for object in objects])}

@app.get("/", response_class=HTMLResponse)
def read_root():
    file_path = './db/models/accueil_content.html'
    with open(file_path, 'r') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

@app.post("/authenticate")
def authenticate(username: str = Form(...),password: str = Form(...)):
    if authentication(username, password):
        return "OKAY BG"
    else:
        return "NOT OKAY BG"