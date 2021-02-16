from cloud_drives.google import GoogleDrive
from config.google import Config

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

google_conf = {
    "CLIENT_ID_JSON" : "token/client_id.json",
    "STORAGE_JSON": "token/storage.json",
    "SCOPES": ['https://www.googleapis.com/auth/drive.readonly.metadata']
}

config = Config(**google_conf)

gdrive = GoogleDrive(config)

@app.get("/list_files")
async def list_files():
    f = await gdrive.list_files()
    return JSONResponse(status_code=200, content=f)



