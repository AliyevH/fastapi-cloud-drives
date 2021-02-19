from inspect import signature
from pydantic import BaseSettings, Field, validator
from typing import List
from pathlib import Path

from pydantic.main import BaseModel
from .errors import AutherizeGoogleClient

from botocore.config import Config

import os

class GoogleDriveConfig(BaseSettings):
    CLIENT_ID_JSON: str = Field(..., env='CLIENT_ID_JSON')
    SCOPES: List[str] = Field(..., env='SCOPES')
    STORAGE_JSON: Path = Field(None, env='STORAGE_JSON')

    class Config:
        case_sensitive = True
    

    @validator("STORAGE_JSON")
    def validate_name(cls,v):
        if not v and  os.path.exists("storage.json"):
            return v
        raise AutherizeGoogleClient("File for authorizing does not exists")


class S3Config(BaseSettings):
    AWS_ACCESS_KEY_ID:                  str = Field(None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY:              str = Field(None, env="AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION:                 str = Field(..., env="AWS_DEFAULT_REGION")
    AWS_CONFIG_FILE:                    str = Field("~/.aws/config", env="AWS_CONFIG_FILE")
    AWS_SHARED_CREDENTIALS_FILE:        str = Field("~/.aws/credentials", env="AWS_SHARED_CREDENTIALS_FILE")
   
    class Config:
        case_sensitive = True
   