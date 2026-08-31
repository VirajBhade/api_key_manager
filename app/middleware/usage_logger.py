from fastapi import Request
import time

from app.database.database import SessionLocal
from app.models.usage_log import Usagelog


async def usage_logger(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    response_time = int((time.time() - start_time) * 1000)

    api_key_id = getattr(request.state, "api_key_id", None)

    if api_key_id is not None:

        db = SessionLocal()

        usage_log = Usagelog(
            api_key_id=api_key_id,
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            response_time=response_time
        )

        db.add(usage_log)
        db.commit()
        db.close()

    return response