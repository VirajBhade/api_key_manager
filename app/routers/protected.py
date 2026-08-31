from fastapi import HTTPException,Depends,APIRouter,Request,Response
from sqlalchemy.orm import Session
import time
from app.dependencies.api_key import get_current_api_key
from app.models.api_key import ApiKey
from app.dependencies.auth import get_db
from app.models.usage_log import Usagelog

router=APIRouter(prefix="/protected_api", tags=["PROTECTED API"])

@router.get("/")
def protected_api(request:Request,response=Response,api_key:ApiKey=Depends(get_current_api_key), db:Session=Depends(get_db)):
    start_time=time.time()
    message="api key is valid"

    response_time = int((time.time() - start_time) * 1000)

    usage_log = Usagelog(
        api_key_id=api_key.id,
        endpoint=request.url.path,
        method=request.method,
        status_code=200,
        response_time=response_time
    )

    db.add(usage_log)
    db.commit()
    db.refresh(usage_log)

    return {
        "message": "message",
        "api_key_id": api_key.id
    }

    
