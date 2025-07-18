from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import authenticate_user
from app.schemas.auth import UserLogin, Token
from app.auth.oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(
        db=db, username=user_credentials.username, password=user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials :3"
        )

    access_token = create_access_token(data={
        "user_id": user.id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
