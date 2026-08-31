from datetime import datetime
from pydantic import BaseModel


class UsageLogResponse(BaseModel):
    id: int
    api_key_id: int
    endpoint: str
    method: str
    status_code: int
    response_time: int
    created_at: datetime