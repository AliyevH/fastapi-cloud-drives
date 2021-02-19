from logging import debug
from fastapi_cloud_drives import GoogleDrive
from fastapi_cloud_drives import GoogleDriveConfig

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
app = FastAPI()

google_conf = {
    "CLIENT_ID_JSON" : "credentials.json",
    "SCOPES": [
        "https://www.googleapis.com/auth/drive"
        ],
    # "STORAGE_JSON": "/home/sabuhi/opt/fastapi-cloud-drives/storage.json"
}

config = GoogleDriveConfig(**google_conf)

gdrive = GoogleDrive(config)

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
