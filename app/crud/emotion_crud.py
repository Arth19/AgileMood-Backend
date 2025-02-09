from sqlalchemy.orm import Session

from app.models.emotion_record_model import EmotionRecord

from app.schemas.emotion_record_schema import EmotionRecordCreate

from app.data_structures import emotion_data_structure as emotions
from .user_crud import get_user_by_id


def get_valid_emotions():
    return emotions.get_valid_emotion()


def create_emotion_record(db: Session, emotion_record: EmotionRecordCreate):
    if not _valid_params(db, emotion_record):
        return None

    db_emotion_record = EmotionRecord(
        user_id=emotion_record.user_id,
        intensity=emotion_record.intensity,
        notes=emotion_record.notes,
        emotion=emotion_record.emotion
    )
    db.add(db_emotion_record)
    db.commit()
    db.refresh(db_emotion_record)

    return db_emotion_record


def _valid_params(db: Session, emotion_record: EmotionRecordCreate) -> bool:
    if get_user_by_id(db, emotion_record.user_id) is None:
        return False
    if not emotions.is_valid_emotion(emotion_record.emotion):
        return False

    return True
