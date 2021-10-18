import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from app.api.routes.router import api_router
from app.core.events import start_app_handler, stop_app_handler
from app.core.config import settings
from app.core.monitoring import instrumentator
from app.core.errors import CustomException
from app.core.logging import CustomizeLogger
from app.core.newrelic import setup_newrelic
import rollbar
import logging

logger = logging.getLogger(__name__)

def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.code, "message": exc.msg}
        )

def get_application() -> FastAPI:
    rollbar.init(settings.ROLLBAR_TOKEN_SECRET_KEY, settings.ROLLBAR_ENV_SECRET_KEY)
    setup_newrelic('/tmp')
    application = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, version=settings.VERSION)
    init_listeners(application)
    instrumentator.instrument(application).expose(application, include_in_schema=False, should_gzip=True)
    application.logger = CustomizeLogger.make_logger()
    application.include_router(api_router)
    application.logger.info("application start")
    application.add_event_handler("startup", start_app_handler(application))
    application.add_event_handler("shutdown", stop_app_handler(application))
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False, debug=False)

