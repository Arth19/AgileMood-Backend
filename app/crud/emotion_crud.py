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


def update_emotion(db: Session, emotion_id: int, emotion_update: dict):
    db_emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if db_emotion is None:
        logger.error(f"Not able to find Emotion with this ID: {emotion_id}")
        return None

    for key, value in emotion_update.items():
        if hasattr(db_emotion, key):
            setattr(db_emotion, key, value)

    db.commit()
    db.refresh(db_emotion)

    logger.debug(f"Emotion with ID {emotion_id} was updated successfully.")
    return db_emotion


def delete_emotion(db: Session, emotion_id: int):
    db_emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if db_emotion is None:
        logger.error(f"Not able to find Emotion with this ID: {emotion_id}")
        return False

    db.delete(db_emotion)
    db.commit()

    logger.debug(f"Emotion with ID {emotion_id} was deleted successfully.")
    return True