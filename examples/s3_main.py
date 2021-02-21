from logging import debug
from fastapi_cloud_drives import S3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastapi_cloud_drives.config import S3Config

app = FastAPI()

s3_config = S3Config(AWS_DEFAULT_REGION="eu-central-1")
s3_client = S3(s3_config)


@app.get("/list_buckets")
async def list_buckets():
    buckets = await s3_client.list_buckets()
    return JSONResponse(status_code=200, content=buckets)

@app.get("/create_bucket")
async def create_bucket():
    created = await s3_client.create_bucket(bucket_name="fastapibucket")
    return JSONResponse(status_code=200, content=created)

@app.get("/upload_file")
async def upload_file():
    created = await s3_client.upload_file(
        bucket_name="fastapibucket", 
        file_name="fastapi.txt",
        object_name="fastapi.txt"
        )
    return JSONResponse(status_code=200, content=created)

@app.get("/download_file")
async def download_file():
    f = await s3_client.download_file(
        bucket_name="fastapibucket", 
        file_name="fastapi.txt", 
        object_name="fastapi.txt"
        )
    return JSONResponse(status_code=200, content=f)