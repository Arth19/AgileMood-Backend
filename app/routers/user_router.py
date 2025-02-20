from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.routers.authentication import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)

from app.models.user_model import UserCreate, UserInDB, UserInTeam
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
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
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


@router.get("/logged", response_model=UserInTeam)
def get_logged_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):

    team_id = user_crud.get_user_team(db, current_user.id)
    result = UserInTeam(
        id=current_user.id, name=current_user.name, email=current_user.email, team_id=team_id
    )

    return result


@router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise Errors.USER_NOT_FOUND
    return db_user


@router.get("/")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise Errors.USER_NOT_FOUND
    return user


@router.put("/", response_model=UserInDB)
def update_user_by_id(
        user_update: dict,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug(f"Call to update emotion by id: {current_user.id}")

    updated_user = user_crud.update_user(db, current_user.id, user_update)
    if updated_user is None:
        logger.error(f"Failed to update emotion with name: {current_user.id}")
        raise Errors.INVALID_PARAMS

    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise Errors.USER_NOT_FOUND
    user_crud.delete_user(db=db, user_id=user_id)
    return Messages.USER_DELETE
