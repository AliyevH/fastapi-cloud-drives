from pydantic import BaseModel
from typing import List

class Config(BaseModel):
    STORAGE_JSON: str
    CLIENT_ID_JSON: str
    SCOPES: List[str]