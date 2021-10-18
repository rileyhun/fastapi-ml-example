from fastapi import APIRouter
from app.models.schemas import HeartbeatResult, StatusResult

router = APIRouter()

@router.get("/health", response_model=HeartbeatResult, name="healthcheck")
async def get_healthcheck() -> HeartbeatResult:
    heartbeat = HeartbeatResult(is_alive=True)
    return heartbeat

@router.get('/ready', response_model=StatusResult, name="readycheck")
async def get_readycheck() -> StatusResult:
    status = StatusResult(is_alive=True)
    return status

@router.get('/status', response_model=StatusResult, name="statuscheck")
async def get_statuscheck() -> StatusResult:
    status = StatusResult(is_alive=True)
    return status


