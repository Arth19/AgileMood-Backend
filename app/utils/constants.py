from fastapi import HTTPException
from http import HTTPStatus


class Errors:
    USER_NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    EMAIL_ALREADY_EXISTS = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists")
    INVALID_PARAMS = HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid params")

    INACTIVE_USER = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Inactive user")
    INCORRECT_CREDENTIALS = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Incorrect username or password")
    CREDENTIALS_EXCEPTION = HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    REPORT_NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Emotion report not found")


class Messages:
    USER_DELETE = {"message": "Used deleted"}


class DataBase:
    DATABASE_URL = "sqlite:///./ma.db"
    EMOTION_RECORDS_TABLE_NAME = "emotion_records"
    EMOTION_TABLE_NAME = "emotion"
    USER_TABLE_NAME = "user"


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240
