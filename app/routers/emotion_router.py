from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.crud import emotion_crud

import app.models.emotion_model as emotion_schema
import app.models.emotion_record_model as emotion_record_schema

from app.models.user_model import UserInDB

from app.databases.sqlite_database import get_db

from app.utils.constants import Errors
from app.utils.logger import logger

from app.routers.authentication import get_current_active_user

router = APIRouter(
    prefix="/emotion",
    tags=["emotion reports"],
)


@router.get("/valid", response_model=emotion_schema.EmotionsResponse)
def get_all_valid_emotions():
    logger.debug("call to get all valid emotions")
    return emotion_crud.get_valid_emotions()


@router.post("/", response_model=emotion_record_schema.EmotionRecord)
def create_emotion_record(
        emotion_record: emotion_record_schema.EmotionRecord,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug("call to create emotion record")

    # Creating emotion Report
    emotion_record.user_id = current_user.id
    response = emotion_crud.create_emotion_record(db, emotion_record)
    if response is None:
        raise Errors.INVALID_PARAMS

    return response


@router.get("/", response_model=emotion_record_schema.AllEmotionReportsResponse)
def get_all_emotion_report_for_logged_user(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    logger.debug("call to get all emotions for logged user id: %s", current_user.id)

    response = emotion_crud.get_emotion_record_by_user_id(db, current_user.id)
    if response is None:
        logger.error(f"no emotion report found for user id: ", current_user.id)
        raise Errors.REPORT_NOT_FOUND
    return {"reports": response}
