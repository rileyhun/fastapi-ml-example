from fastapi import APIRouter
from app.api.routes import prediction, healthcheck, index
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(healthcheck.router, tags=["health"], prefix=f"{settings.PREFIX}/status")
api_router.include_router(prediction.router, tags=["predictor"], prefix=settings.PREFIX)
api_router.include_router(index.router, tags=["index"])