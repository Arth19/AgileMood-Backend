from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas.user_schema as user_schema

from app.crud import user_crud
from app.databases.sqlite_database import get_db
from app.utils.constants import Errors, Messages

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}", response_model=user_schema.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise Errors.USER_NOT_FOUND
    return db_user


@router.post("/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise Errors.EMAIL_ALREADY_EXISTS
    return user_crud.create_user(db=db, user=user)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise Errors.USER_NOT_FOUND
    user_crud.delete_user(db=db, user_id=user_id)
    return Messages.USER_DELETE
