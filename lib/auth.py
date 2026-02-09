from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional, cast

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from db.session import get_db
from models.user import User
from schemas.tokenSchema import TokenData

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(password_hash.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return cast(str, password_hash.hash(password))


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user: Optional[User] = result.scalar_one_or_none()

    if user is None:
        return None

    if user.password is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(
    data: dict[str, object],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode: dict[str, object] = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return cast(str, encoded_jwt)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        username = payload.get("sub")
        if not isinstance(username, str):
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    stmt = select(User).where(User.username == token_data.username)
    result = await db.execute(stmt)
    user: Optional[User] = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.deleted_at is not None:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
