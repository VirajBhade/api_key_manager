from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class APIKeyCreate(BaseModel):
    name: str
    rate_limit: int = 100
    expires_at: Optional[datetime] = None


class APIKeyResponse(BaseModel):
    id: int
    name: str
    api_key: Optional[str] = None
    prefix: str
    status: str
    rate_limit: int
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True