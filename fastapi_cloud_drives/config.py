from pydantic import BaseModel
from typing import List
from pathlib import Path


class GoogleDriveConfig(BaseModel):
    CLIENT_ID_JSON: str
    SCOPES: List[str]
    STORAGE_JSON: Path = None

