from hashlib import sha256

from sqlalchemy.orm import Session
from app.schemas.user_schema import User as UserModel
from app.models.user_model import User, UserInDB

from app.utils.logger import logger


def get_user_by_id(db: Session, user_id: int) -> UserInDB | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserInDB | None:
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user: User):
    db_user = _response_to_db_model(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db.delete(user)
    db.commit()


def _response_to_db_model(user: User) -> UserModel:
    return UserModel(
        name=user.name,
        email=user.email,
        disabled=False,
        hashed_password=get_password_hash(user.password),
    )


def get_password_hash(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()
