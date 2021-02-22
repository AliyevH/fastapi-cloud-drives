<h3 align="center">FastAPI Cloud Drives</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/MadeByMads/fastapi-cloud-drives/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/MadeByMads/fastapi-cloud-drives/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>


## 🧐 About <a name = "about"></a>
The FastAPI Cloud Drives module supports AWS S3, Google Drive, Dropbox cloud storage providers. You can easily search, upload, download files from this cloud providers. 

### Configuration
By default this module can get configurations from environment variables:
* `AWS_ACCESS_KEY_ID`:
* `AWS_SECRET_ACCESS_KEY`:
* `AWS_DEFAULT_REGION`:                        `REQUIRED`
* `AWS_CONFIG_FILE`:                                `Default: ~/.aws/config`
* `AWS_SHARED_CREDENTIALS_FILE`:    `Default: ~/.aws/credentials`
   
If `~/.aws/credentials` and `~/.aws/config` exists you don't need additional settings.

Only `AWS_DEFAULT_REGION` is required as environment or by argument to `S3Config` as shown in example below


### Example:

```python
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
        bucket_name="fastapibucket", # bucket_name: S3 Bucket to upload
        file_name="fastapi.txt",     # file_name:   Path to file
        object_name="fastapi.txt"    # object_name: Name of file to save in S3 Bucket
        )
    return JSONResponse(status_code=200, content=f)

@app.get("/list_objects")
async def list_objects():
    page_iterator = await s3_client.list_objects(bucket_name="fastapibucket")
    for page in page_iterator:
        print(page.get("Contents"))
    return JSONResponse(status_code=200)
```

### Step 3
Run application:
```python
uvicorn main:app --reload
```