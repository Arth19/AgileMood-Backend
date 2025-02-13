from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.routers.authentication import authenticate_user, create_access_token

from app.models.user_model import UserCreate, UserInDB
from app.models.token_model import Token

from app.crud import user_crud
from app.databases.sqlite_database import get_db
from app.utils.constants import Errors, Messages
from app.utils.logger import logger


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    if not authenticate_user(db, form_data.username, form_data.password):
        raise Errors.INCORRECT_CREDENTIALS

    access_token = create_access_token({"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("Call to create User")
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise Errors.EMAIL_ALREADY_EXISTS

    response = user_crud.create_user(db=db, user=user)
    if response is None:
        raise Errors.INVALID_PARAMS
    return response


@router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise Errors.USER_NOT_FOUND
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise Errors.USER_NOT_FOUND
    user_crud.delete_user(db=db, user_id=user_id)
    return Messages.USER_DELETE
