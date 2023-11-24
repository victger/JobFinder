from pydantic import BaseModel
from datetime import timedelta
from minio import Minio
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

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
    html_content = """
    <html>
        <head>
            <title>Hello user</title>
            <style>
                body {
                    background-color: #3498db;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    color: white;
                }
                form {
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 300px;
                }
            </style>
        </head>
        <body>
            <center>
            <h1>Hello user</h1>
            <form action="/authenticate" method="post">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" style="width: 100%; margin-bottom: 10px;">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" style="width: 100%; margin-bottom: 10px;">
                <button type="submit" style="width: 100%;">Submit</button>
            </form>
            </center>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/authenticate")
def authenticate(username: str = Form(...),password: str = Form(...)):
    # Validate the entered password (replace this with your own authentication logic)
    if password == "abcde":
        return {"message": "Authentication successful"}
    else:
        return {"message": "Authentication failed"}