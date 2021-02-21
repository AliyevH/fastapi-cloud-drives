from pydantic import BaseSettings, Field, validator
from typing import List
from pathlib import Path
from .errors import AutherizeGoogleClient
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





class DropBoxConfig(BaseSettings):
    DROPBOX_TOKEN: str = Field(..., env='DROPBOX_TOKEN')
    APP_KEY: str =  Field(..., env='APP_KEY')
    APP_SECRET: str = Field(...,env='APP_SECRET')

    class Config:
        case_sensitive = True
    