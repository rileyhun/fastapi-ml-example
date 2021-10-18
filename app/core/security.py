from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.core.config import settings
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from typing import Optional
import secrets

api_key = APIKeyHeader(name=settings.AUTH_TOKEN_HEADER_KEY, auto_error=False)

def check_authentication_header(header: Optional[str] = Security(api_key)) -> bool:
    """ takes the X-API-Key header and converts it into the matching user object from the database """

    if header is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="No API key provided.", headers={}
        )

    if not secrets.compare_digest(header, str(settings.AUTH_TOKEN_SECRET_KEY)):

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid API key", headers={}
        )
    return True