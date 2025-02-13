from sqlalchemy.orm import Session

from app.schemas.emotion_record_schema import EmotionRecord
from app.data_structures import emotion_data_structure as emotions

from app.utils.logger import logger


def get_valid_emotions():
    return emotions.get_valid_emotion()


def create_emotion_record(db: Session, emotion_record: EmotionRecord):
    if not _valid_params(emotion_record):
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


def get_emotion_record_by_user_id(db: Session, user_id: int):
    return db.query(EmotionRecord).filter(EmotionRecord.user_id == user_id).all()


def _valid_params(emotion_record: EmotionRecord) -> bool:
    if not emotions.is_valid_emotion(emotion_record.emotion):
        logger.debug("Invalid emotion: %s", emotion_record.emotion)
        return False

    if not 0 <= emotion_record.intensity <= 5:
        logger.debug("Invalid intensity: %s", emotion_record.intensity)
        return False

    return True
