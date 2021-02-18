from pydantic import BaseModel
from typing import List

class GoogleDriveConfig(BaseModel):
    CLIENT_ID_JSON: str
    SCOPES: List[str]