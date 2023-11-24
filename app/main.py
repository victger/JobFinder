from datetime import timedelta
from minio import Minio
from fastapi import FastAPI, File, UploadFile, Form, HTMLResponse
from db.services import authentication
from db.models import accueil_content as html_content

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)

client = Minio("minio:9000", "root", "rootpassword", secure=False)

@app.post('/file/upload/')
async def upload_file(file: UploadFile = File(...)):
    result = client.put_object("name", file.filename, file.file, 5000)
    return {'result': result}

@app.put('/file/presigned/')
async def put_presigned_file(name: str):
    put_url = client.get_presigned_url(
        "GET",
        "name",
        name,
        expires=timedelta(days=1),
        response_headers={"response-content-type": "application/json"},
    )
    return put_url

@app.get('/bucket/show/')
async def show_bucket(name: str):
    objects = client.list_objects(name, recursive=True)
    return {'result': '\n'.join([object.object_name for object in objects])}

@app.get("/", response_class=HTMLResponse)
def read_root():
    accueil_content = html_content
    return HTMLResponse(content=accueil_content, status_code=200)

@app.post("/authenticate")
def authenticate(username: str = Form(...),password: str = Form(...)):
    if authentication(username, password):
        return "OKAY BG"
    else:
        return "NOT OKAY BG"