from sqlalchemy.orm import Session

from app.schemas.emotion_record_schema import EmotionRecord

from app.utils.logger import logger


def create_emotion_record(db: Session, emotion_record: EmotionRecord):
    db_emotion_record = EmotionRecord(
        user_id=emotion_record.user_id,
        emotion_id=emotion_record.emotion_id,
        intensity=emotion_record.intensity,
        notes=emotion_record.notes,
    )
    db.add(db_emotion_record)
    db.commit()
    db.refresh(db_emotion_record)

    return db_emotion_record


def get_emotion_records_by_user_id(db: Session, user_id: int):
    return db.query(EmotionRecord).filter(EmotionRecord.user_id == user_id).all()


def get_emotion_records_by_user_id_and_emotion_id(db: Session, user_id: int, emotion_id: int):
    return db.query(EmotionRecord).filter(EmotionRecord.user_id == user_id, EmotionRecord.emotion_id == emotion_id).all()
