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

@app.get('/bucket/show/')
async def show_bucket(name: str):
    objects = client.list_objects(name, recursive=True)
    return {'result': '\n'.join([object.object_name for object in objects])}

@app.get("/", response_class=HTMLResponse)
def read_root():
<<<<<<< HEAD:app/main.py
    accueil_content = html_content
    return HTMLResponse(content=accueil_content, status_code=200)
=======
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
            .download-btn {
                width: 100%;
                margin-top: 10px;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
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
            <button onclick="downloadFile()">Download File</button>
        </center>
        <script src="script.js"></script>
    </body>
</html>

    """
    return HTMLResponse(content=html_content, status_code=200)
>>>>>>> d670075dc782fbee2a47398b2f6c4626ccf91b60:app/front/main.py

@app.post("/authenticate")
def authenticate(username: str = Form(...),password: str = Form(...)):
    if authentication(username, password):
        return "OKAY BG"
    else:
        return "NOT OKAY BG"