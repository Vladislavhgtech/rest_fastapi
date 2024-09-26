from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta

from security.pwdcrypt import verify_password
from models.models import User, Role, AuthUser
from db.db import get_user
import config as config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(username: str, password: str):
    db_user = get_user(username)
    if db_user is None or not verify_password(password, db_user.password):
        return None
    return db_user


def get_exp() -> datetime:
    return datetime.utcnow() + timedelta(seconds=config.EXPIRATION_TIME_SECONDS)


def create_jwt_token(user: User) -> str:
    data = {
        "sub": user.username,
        "role": user.role.name,
        "exp": get_exp()
    }
    return jwt.encode(data, config.SECRET_KEY, algorithm=config.ALGORITHM)


def get_authuser_from_token(token: str = Depends(oauth2_scheme)) -> AuthUser:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return AuthUser(username=payload.get("sub"), role=Role[payload.get("role")])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )