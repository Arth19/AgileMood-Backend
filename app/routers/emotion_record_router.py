from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.crud import emotion_record_crud
from app.crud import emotion_crud

import app.models.emotion_model as emotion_model
import app.models.emotion_record_model as emotion_record_model

from app.models.user_model import UserInDB

from app.databases.sqlite_database import get_db

from app.utils.constants import Errors
from app.utils.logger import logger

from app.routers.authentication import get_current_active_user

router = APIRouter(
    prefix="/emotion_record",
    tags=["emotion records"],
)


@router.post("/", response_model=emotion_record_model.EmotionRecordInDb)
def create_emotion_record(
        emotion_record: emotion_record_model.EmotionRecord,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug("call to create emotion record")

    # Creating emotion Report
    emotion_record.user_id = current_user.id
    response = emotion_record_crud.create_emotion_record(db, emotion_record)
    if response is None:
        raise Errors.INVALID_PARAMS

    return response


@router.get("/", response_model=emotion_record_model.AllEmotionReportsResponse)
def get_all_emotion_report_for_logged_user(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug("call to get all emotion records")

    response = emotion_record_crud.get_emotion_records_by_user_id(db, current_user.id)
    if response is None:
        logger.error(f"no emotion record found in the database")
        raise Errors.REPORT_NOT_FOUND
    return {"emotion_records": response}


@router.get("/{emotion_name}", response_model=emotion_record_model.AllEmotionReportsResponse)
def get_emotion_report_for_logged_user_by_emotion_name(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        emotion_name: str,
        db: Session = Depends(get_db),
):
    logger.debug("call to get emotions records by emotion name")

    emotion_id = emotion_crud.get_emotion_id_by_name(emotion_name)
    response = emotion_record_crud.get_emotion_records_by_user_id_and_emotion_id(db, current_user.id, emotion_id)
    if response is None:
        logger.error(f"no emotion record found in the database for this emotion name: {emotion_name}")
        raise Errors.REPORT_NOT_FOUND
    return {"emotion_records": response}