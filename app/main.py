from fastapi import FastAPI, Request

from app.routers import auth
from app.routers import api_keys
from app.routers import protected
from app.routers import analytics

from app.models.user import User
from app.models.api_key import ApiKey
from app.models.usage_log import Usagelog

from app.middleware.usage_logger import usage_logger






app = FastAPI(title="API Key Manager")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    return await usage_logger(request, call_next)


app.include_router(auth.router)
app.include_router(api_keys.router)
app.include_router(protected.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {
        "message": "API Key manager is running"
    }