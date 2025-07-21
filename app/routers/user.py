from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.db_raw import get_connection
from app.core.db import get_db
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse, UserUpdate
from app.models.user import User as user_model
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password minimal 8 karakter."
        )

    # hash the password (bcrypt hashing)
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = user_model(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()

        # refresh to get DB-generated fields
        db.refresh(new_user)

        return new_user

    except IntegrityError as e:
        db.rollback()  # prevent db broken
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User dengan username tersebut sudah ada."
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    query = db.query(user_model)
    users = query.all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    query = db.query(user_model).filter(user_model.id == id)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
