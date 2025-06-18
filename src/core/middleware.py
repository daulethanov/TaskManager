import jwt
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from src.core.config import cfg

api_key_header = APIKeyHeader(name="Authorization", auto_error=False, description="Enter token",)


def verify_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, cfg.JWT_SECRET_KEY, algorithms=cfg.JWT_ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def user_middleware(auth_header: str = Depends(api_key_header)):
    if auth_header is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = auth_header
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    payload = verify_jwt(token)
    return payload
