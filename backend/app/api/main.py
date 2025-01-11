from fastapi import APIRouter, FastAPI

from backend.app.core.config import settings
from backend.app.api.routes import timestamp

app = FastAPI()

app.include_router(timestamp.router)
