from pydantic import BaseModel
from typing import List

class GDriveConfig(BaseModel):
    CREDENTIALS_JSON: str
    STORAGE_JSON: str
    CLIENT_ID_JSON: str
    SCOPES: List[str]