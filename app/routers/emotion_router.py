from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import emotion_crud

import app.schemas.emotion_schema as emotion_schema
import app.schemas.emotion_record_schema as emotion_record_schema

from app.databases.sqlite_database import get_db

from app.utils.constants import Errors

router = APIRouter(
    prefix="/emotion",
    tags=["emotion"],
)


@router.get("/", response_model=emotion_schema.EmotionsResponse)
def get_all_valid_emotions():
    return emotion_crud.get_valid_emotions()


@router.post("/", response_model=emotion_record_schema.EmotionRecordResponse)
def create_emotion_record(emotion_record: emotion_record_schema.EmotionRecordCreate, db: Session = Depends(get_db)):
    response = emotion_crud.create_emotion_record(db, emotion_record)
    if response is None:
        raise Errors.INVALID_PARAMS
    return response
