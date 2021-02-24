from logging import debug
from fastapi_cloud_drives import GoogleDrive
from fastapi_cloud_drives import GoogleDriveConfig

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
app = FastAPI()

# google_conf = {
#     "CLIENT_ID_JSON" : "client_id.json",
#     "SCOPES": [
#         "https://www.googleapis.com/auth/drive"
#         ],
#     # "STORAGE_JSON": "/home/sabuhi/opt/fastapi-cloud-drives/storage.json"
# }

# config = GoogleDriveConfig(**google_conf)

# gdrive = GoogleDrive(config)

# @app.get("/list_files")
# async def list_files():
#     f = await gdrive.list_files()
#     return JSONResponse(status_code=200, content=f)

# @app.get("/upload_file")
# async def upload_file():
#     resp = await gdrive.upload_file(
#         filename = "photo.jpg",
#         filepath = "files/photo.jpg",
#     )
#     return JSONResponse(status_code=200, content=resp)

# @app.get("/create_folder")
# async def create_folder():
#     resp = await gdrive.create_folder(folder_name="Examples")
#     return JSONResponse(status_code=200, content=resp)

# @app.get("/download_file")
# async def download_file():
#     r = await gdrive.download_file(file_name = "photo.jpeg")
#     return JSONResponse(status_code=200, content=r)


from logging import debug
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from starlette.requests import Request
from fastapi_cloud_drives import DropBoxConfig, DropBox
from starlette.middleware.sessions import SessionMiddleware
from dropbox import DropboxOAuth2Flow
from starlette.responses import RedirectResponse
import os

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="my_secret")

REDIRECT_URI = "http://127.0.0.1:8020/auth"


conf  = DropBoxConfig(
    APP_KEY="",
    APP_SECRET="")


def dropbox_auth_flow(session):

   
    return DropboxOAuth2Flow(
       consumer_key=conf.APP_KEY ,redirect_uri=REDIRECT_URI,consumer_secret=conf.APP_SECRET, token_access_type="offline", session=session,  csrf_token_session_key="dropbox-auth-csrf-token")

def dropbox_auth_start(session):
    authorize_url = dropbox_auth_flow(session).start()

    return RedirectResponse(authorize_url)

def dropbox_auth_finish(session, request):
    try:
        print("CONF", conf)

        response = dropbox_auth_flow(session).finish(request.query_params)
    
        os.environ['DROPBOX_REFRESH_TOKEN'] = response.refresh_token
        os.environ['DROPBOX_ACCESS_TOKEN'] = response.access_token

        conf.DROPBOX_REFRESH_TOKEN =  response.refresh_token
        conf.DROPBOX_ACCESS_TOKEN =  response.access_token
        return JSONResponse(status_code=200, content={"result": True})

    except Exception  as err:
        print(err)
        return JSONResponse(status_code=404, content={"result": False})


@app.get("/")
async def dropbox_auth(request: Request):

    return dropbox_auth_start(request.session)

@app.get("/auth")
async def finish_auth(request: Request):
    
    return dropbox_auth_finish(request.session,request)

  


@app.get("/list_buckets")
async def list_buckets():

    async with DropBox(conf) as drop:
        result = await drop.list_files("/path")

    return JSONResponse(status_code=200, content=result)


@app.get("/account")
async def account_info():
  
    async with DropBox(conf) as drop:
        result = await drop.account_info()

    return JSONResponse(status_code=200, content=result)



@app.get("/linktofile")
async def create_bucket():
    async with DropBox(conf) as drop:
        result = await drop.get_link_of_file("/path/", "file.JPG")

    return JSONResponse(status_code=200, content=result)

@app.get("/savefile")
async def create_bucket():
    async with DropBox(conf) as drop:
        await drop.save_file_localy("/path/", "file.JPG")

    return JSONResponse(status_code=200, content={"result:": True})




@app.get("/upload_file")
async def upload_file():
    async with DropBox(conf) as drop:

        await drop.upload_file(
            file_from="file.py",
            file_to="/path"
        )

    return JSONResponse(status_code=200, content={"result":True})


