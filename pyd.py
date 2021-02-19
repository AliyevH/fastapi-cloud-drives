
from typing import Set
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    api_key: str = Field(...)

s = Settings()
print(s.dict())