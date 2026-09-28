import logging
import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy import select

from .database import SessionLocal
from .models import User

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"
TOKEN_TTL_HOURS = 8
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

_DEV_SECRET = "local-development-secret-change-before-production"


def jwt_secret() -> str:
    """Resolve the token-signing key.

    A missing JWT_SECRET falls back to a well-known value so the local seeded
    demo runs out of the box. That fallback is a real risk, so it is announced
    loudly at startup rather than applied quietly. Every deployed instance must
    set JWT_SECRET.
    """
    configured = os.getenv("JWT_SECRET", "").strip()
    if not configured:
        return _DEV_SECRET
    return configured


if not os.getenv("JWT_SECRET", "").strip():
    logger.warning(
        "SECURITY: JWT_SECRET is not set. Tokens are being signed with a publicly "
        "known development key. Set JWT_SECRET on every deployed instance."
    )


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_access_token(user: User) -> str:
    expires_at = datetime.now(UTC) + timedelta(hours=TOKEN_TTL_HOURS)
    return jwt.encode(
        {"sub": user.id, "role": user.role, "exp": expires_at},
        jwt_secret(),
        algorithm=ALGORITHM,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, jwt_secret(), algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except jwt.PyJWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired access token") from exc
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid access token")
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer exists")
        session.expunge(user)
        return user


def require_roles(*roles: str):
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Your role cannot perform this action")
        return user

    return dependency
