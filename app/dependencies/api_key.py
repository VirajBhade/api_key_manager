from datetime import datetime,timezone

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.api_key import ApiKey
from app.core.security import verify_api_key
from app.dependencies.rate_limit import check_rate_limit


security = HTTPBearer()


def get_current_api_key(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    # 1. Get the actual API key from Authorization header
    api_key = credentials.credentials

    # 2. Extract prefix
    prefix = api_key[:8]

    # 3. Find API key record using prefix
    api_key_record = (
        db.query(ApiKey)
        .filter(ApiKey.prefix == prefix)
        .first()
    )
    print("API KEY RECEIVED:", api_key)
    print("PREFIX:", prefix)
    print("RECORD:", api_key_record)

    # 4. Key doesn't exist
    if api_key_record is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # 5. Verify API key against stored hash
    if not verify_api_key(api_key, api_key_record.key_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # 6. Check whether key is active
    if api_key_record.status != "active":
        raise HTTPException(
            status_code=401,
            detail="API key is not active"
        )

    # 7. Check expiration
    if (
        api_key_record.expires_at is not None
        and api_key_record.expires_at < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=401,
            detail="API key has expired"
        )

    request.state.api_key_id = api_key_record.id

    check_rate_limit(
    api_key_record.id,
    api_key_record.rate_limit
)

    return api_key_record