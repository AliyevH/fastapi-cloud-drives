<h3 align="center">FastAPI Cloud Drives</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/MadeByMads/fastapi-cloud-drives/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/MadeByMads/fastapi-cloud-drives/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>


## 🧐 About <a name = "about"></a>

The FastAPI Cloud Drives module supports Google Drive, OneDrive, Dropbox cloud storage providers. You can easily search, upload, download files from this cloud providers. 

### Step 1
Go to link https://developers.google.com/drive/api/v3/quickstart/python
Enable Drive Api.
Download credentials.json file

### Step 2
Before deploying app to production you need one time approve and give permission.
Run:
```python
python main.py --noauth_local_webserver
```
Follow instruction, get verification code from Google and paste it in terminal. 
After successful authentication, module will create ```storage.json``` file. 

If you change permissions in Google Cloud for the application, you need repeat Step 2 again.

### Step 3
Run application:
```python
uvicorn main:app --reload
```

### Example:

```python
from fastapi_cloud_drives.FastAPIGoogle import GoogleDrive
from fastapi_cloud_drives.config import GoogleDriveConfig

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

google_conf = {
    "CLIENT_ID_JSON" : "client_id.json",
    "SCOPES": [
        "https://www.googleapis.com/auth/drive"
        ]
}

config = GoogleDriveConfig(**google_conf)

app = FastAPI()

@app.get("/list_files")
async def list_files():
    f = await gdrive.list_files()
    return JSONResponse(status_code=200, content=f)

@app.get("/upload_file")
async def upload_file():
    resp = await gdrive.upload_file(
        filename = "photo.jpg",
        filepath = "files/photo.jpg",
    )
    return JSONResponse(status_code=200, content=resp)

@app.get("/create_folder")
async def create_folder():
    resp = await gdrive.create_folder(folder_name="Examples")
    return JSONResponse(status_code=200, content=resp)

@app.get("/download_file")
async def download_file():
    r = await gdrive.download_file(file_name = "photo.jpeg")
    return JSONResponse(status_code=200, content=r)
```

```CLIENT_ID_JSON``` is a file that you download from Google Cloud.

For more information about ```SCOPES``` go to: https://developers.google.com/identity/protocols/oauth2/scopes
