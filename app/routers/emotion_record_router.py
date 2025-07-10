from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends

from app.crud import emotion_record_crud
from app.crud import emotion_crud

from app.models.emotion_record_model import (
    EmotionRecordInDb,
    EmotionRecord,
    AllEmotionReportsResponse,
)

from app.models.user_model import UserInDB

from app.routers.authentication import get_current_active_user

from app.databases.postgres_database import get_db

from app.utils.constants import Errors, Role
from app.utils.logger import logger


router = APIRouter(
    prefix="/emotion_record",
    tags=["emotion records"],
)


@router.post("/", response_model=EmotionRecordInDb)
def create_emotion_record(
    emotion_record: EmotionRecord,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logger.debug("call to create emotion record")

    emotion_record.user_id = current_user.id
    response = emotion_record_crud.create_emotion_record(db, emotion_record)
    if response is None:
        raise Errors.INVALID_PARAMS

    return response


@router.get("/", response_model=AllEmotionReportsResponse)
def get_all_emotion_report_for_logged_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    include_feedbacks: bool = False,
):
    logger.debug("call to get all emotion records")

    response = emotion_record_crud.get_emotion_records_by_user_id(
        db, [current_user.id], for_team=False, include_feedbacks=include_feedbacks
    )
    if response is None:
        logger.error(f"no emotion record found in the database")

    return AllEmotionReportsResponse(emotion_records=response)


@router.get("/{emotion_name}", response_model=AllEmotionReportsResponse)
def get_emotion_report_for_logged_user_by_emotion_name(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    emotion_name: str,
    db: Session = Depends(get_db),
    include_feedbacks: bool = False,
):
    logger.debug("call to get emotions records by emotion name")

    emotion_id = emotion_crud.get_emotion_id_by_name(db, emotion_name)
    response = emotion_record_crud.get_emotion_records_by_user_id_and_emotion_id(
        db, current_user.id, emotion_id, include_feedbacks=include_feedbacks
    )
    if response is None:
        logger.error(
            f"no emotion record found in the database for this emotion name: {emotion_name}"
        )
        raise Errors.NOT_FOUND
    return AllEmotionReportsResponse(emotion_records=response)


@router.get("/id/{record_id}", response_model=EmotionRecordInDb)
def get_emotion_record_by_id(
    record_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    logger.debug("call to get emotion record by id")
    record = emotion_record_crud.get_emotion_record_by_id(db, record_id)
    if record is None or record.user_id != current_user.id:
        raise Errors.NOT_FOUND
    return record
