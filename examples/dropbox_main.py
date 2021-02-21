from logging import debug
from fastapi_cloud_drives import S3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastapi_cloud_drives import DropBoxConfig, DropBox

app = FastAPI()

conf  = DropBoxConfig(DROPBOX_TOKEN="your_token",
APP_KEY="your_key",
APP_SECRET="your_secret")







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
