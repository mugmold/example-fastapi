from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordBearer
from app.core.db import get_db
from app.models.user import User as user_model
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(
            token=token, key=SECRET_KEY, algorithms=ALGORITHM
        )

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = TokenData(id=id)

        return token_data
    except JWTError:
        raise credential_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(
        token=token, credential_exception=credential_exception)

    user = db.query(user_model).filter(user_model.id == token_data.id).first()

    if not user:
        raise credential_exception

    return user
