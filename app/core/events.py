from app.services.predict import MachineLearningModelHandlerScore
from fastapi import FastAPI
from typing import Callable
from loguru import logger

def _startup_model(app: FastAPI) -> None:
    model_instance = MachineLearningModelHandlerScore()
    app.state.model = model_instance

def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None

def start_app_handler(app: FastAPI) -> Callable:
    async def startup() -> None:
        logger.debug("loading in model ...")
        _startup_model(app)
    return startup

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)
    return shutdown