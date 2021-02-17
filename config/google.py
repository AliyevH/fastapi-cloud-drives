from google.auth.environment_vars import CREDENTIALS
from pydantic import BaseModel
from typing import List

class Config(BaseModel):
    CREDENTIALS_JSON: str
    STORAGE_JSON: str
    CLIENT_ID_JSON: str
    SCOPES: List[str]