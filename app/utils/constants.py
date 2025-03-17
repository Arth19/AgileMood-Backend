from fastapi import HTTPException
from http import HTTPStatus


class Errors:
    INACTIVE_USER = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Inactive user")
    EMAIL_ALREADY_EXISTS = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists")
    INVALID_PARAMS = HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid params")
    NO_PERMISSION = HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                  detail="You have no permission to do that, contact your manager")

    INCORRECT_CREDENTIALS = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Incorrect username or password")
    CREDENTIALS_EXCEPTION = HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND)


class Messages:
    USER_DELETE = {"message": "Used deleted"}
    EMOTION_DELETE = {"message": "Emotion deleted"}
    MEMBER_ADDED_TO_TEAM = {"message": "Member added successfully!"}
    MEMBER_REMOVED_FROM_TEAM = {"message": "Member removed successfully!"}
    FEEDBACK_SENT = {"message": "Feedback sent successfully!"}


class DataBase:
    DATABASE_URL = "sqlite:///./ma.db"
    EMOTION_RECORDS_TABLE_NAME = "emotion_record"
    EMOTION_TABLE_NAME = "emotion"
    USER_TABLE_NAME = "user"
    TEAM_TABLE_NAME = "team"
    FEEDBACK_TABLE_NAME = "feedback"


class Role:
    MANAGER = "manager"
    EMPLOYEE = "employee"


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240
