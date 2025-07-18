from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User as user_model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(user_model).filter(user_model.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
