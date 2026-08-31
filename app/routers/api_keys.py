from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.api_key import ApiKey
from app.models.user import User
from app.schemas.api_key import APIKeyCreate, APIKeyResponse
from app.core.security import generate_api_key, hash_api_key


router = APIRouter(
    prefix="/api_keys",
    tags=["API Keys"]
)


@router.post("/", response_model=APIKeyResponse)
def create_api_key(
    api_key_data: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1. Generate actual API key
    actual_api_key = generate_api_key()

    # 2. Hash the actual API key
    hashed_api_key = hash_api_key(actual_api_key)

    # 3. Get prefix
    prefix = actual_api_key[:8]

    # 4. Create database record
    new_api_key = ApiKey(
        user_id=current_user.id,
        name=api_key_data.name,
        key_hash=hashed_api_key,
        status="active",
        prefix=prefix,
        rate_limit=api_key_data.rate_limit,
        expires_at=api_key_data.expires_at
    )

    # 5. Save to database
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)

    # 6. Return the actual key
    return {
        "id": new_api_key.id,
        "name": new_api_key.name,
        "api_key": actual_api_key,
        "prefix": new_api_key.prefix,
        "status": new_api_key.status,
        "rate_limit": new_api_key.rate_limit,
        "expires_at": new_api_key.expires_at,
        "created_at": new_api_key.created_at
    }
    

# GET ALL API KEYS
@router.get("/", response_model=list[APIKeyResponse])
def get_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_keys = (
        db.query(ApiKey)
        .filter(ApiKey.user_id == current_user.id)
        .all()
    )

    return api_keys


# GET ONE API KEY
@router.get("/{api_key_id}", response_model=APIKeyResponse)
def get_api_key(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.id == api_key_id,
            ApiKey.user_id == current_user.id
        )
        .first()
    )

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found"
        )

    return api_key


# REVOKE API KEY
@router.patch("/{api_key_id}/revoke")
def revoke_api_key(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.id == api_key_id,
            ApiKey.user_id == current_user.id
        )
        .first()
    )

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found"
        )

    api_key.status = "revoked"

    db.commit()
    db.refresh(api_key)

    return {
        "message": "API key revoked successfully"
    }


# DELETE API KEY
@router.delete("/{api_key_id}")
def delete_api_key(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.id == api_key_id,
            ApiKey.user_id == current_user.id
        )
        .first()
    )

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found"
        )

    db.delete(api_key)
    db.commit()

    return {
        "message": "API key deleted successfully"
    }