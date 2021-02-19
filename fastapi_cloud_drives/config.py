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



