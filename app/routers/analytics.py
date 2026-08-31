from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.usage_log import Usagelog
from app.models.api_key import ApiKey


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    usage_logs = (
        db.query(Usagelog)
        .join(
            ApiKey,
            Usagelog.api_key_id == ApiKey.id
        )
        .filter(
            ApiKey.user_id == current_user.id
        )
        .all()
    )

    total_requests = len(usage_logs)

    successful_requests = sum(
        1 for log in usage_logs
        if log.status_code < 400
    )

    failed_requests = sum(
        1 for log in usage_logs
        if log.status_code >= 400
    )

    if total_requests > 0:
        average_response_time = sum(
            log.response_time for log in usage_logs
        ) / total_requests
    else:
        average_response_time = 0

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "average_response_time": average_response_time
    }