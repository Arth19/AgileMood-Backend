from sqlalchemy.orm import Session

from app.schemas.emotion_record_schema import Emotion

from app.utils.logger import logger


def create_emotion(db: Session, emotion: Emotion):
    db_emotion = Emotion(
        name=emotion.name,
        emoji=emotion.emoji,
        color=emotion.color
    )
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)

    return db_emotion


def get_emotion_by_id(db: Session, id: int):
    return db.query(Emotion).filter(Emotion.id == id).first()


def get_emotion_id_by_name(db: Session, name: str):
    return db.query(Emotion).filter(Emotion.name == name).first()


def get_all_emotions(db: Session):
    return db.query(Emotion).all()
