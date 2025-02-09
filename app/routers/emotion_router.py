from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import emotion_crud
from app.crud import user_crud

import app.schemas.emotion_schema as emotion_schema
import app.schemas.emotion_record_schema as emotion_record_schema

from app.databases.sqlite_database import get_db

from app.utils.constants import Errors
from app.utils.logger import logger


router = APIRouter(
    prefix="/emotion",
    tags=["emotion reports"],
)


@router.get("/", response_model=emotion_schema.EmotionsResponse)
def get_all_valid_emotions():
    logger.debug("call to get all valid emotions")
    return emotion_crud.get_valid_emotions()


@router.post("/", response_model=emotion_record_schema.EmotionRecordResponse)
def create_emotion_record(emotion_record: emotion_record_schema.EmotionRecordCreate, db: Session = Depends(get_db)):
    logger.debug("call to create emotion record")

    # Checking if user exists
    if user_crud.get_user_by_id(db, emotion_record.user_id) is None:
        logger.error("user %s do not exist", emotion_record.user_id)
        raise Errors.USER_NOT_FOUND

    # Creating emotion Report
    response = emotion_crud.create_emotion_record(db, emotion_record)
    if response is None:
        raise Errors.INVALID_PARAMS

    return response


@router.get("/{user_id}", response_model=emotion_record_schema.AllEmotionReportsResponse)
def get_all_emotion_report_by_user_id(user_id: int, db: Session = Depends(get_db)):
    logger.debug("call to  get all emotions by user id: %s", user_id)

    response = emotion_crud.get_emotion_record_by_user_id(db, user_id)
    if response is None:
        logger.error(f"no emotion report found for user id: ", user_id)
        raise Errors.REPORT_NOT_FOUND
    return {"reports": response}
