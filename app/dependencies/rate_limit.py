from fastapi import HTTPException
from datetime import datetime, timedelta


request_history = {}

TIME_WINDOW = 60


def check_rate_limit(api_key_id: int, rate_limit: int):

    now = datetime.utcnow()

    if api_key_id not in request_history:
        request_history[api_key_id] = []

    request_history[api_key_id] = [
        request_time
        for request_time in request_history[api_key_id]
        if now - request_time < timedelta(seconds=TIME_WINDOW)
    ]

    if len(request_history[api_key_id]) >= rate_limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    request_history[api_key_id].append(now)