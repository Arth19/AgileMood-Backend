from sqlalchemy.orm import Session

from app.models.emotion_record_model import EmotionRecord as EmotionRecordModel
from app.models.emotion_record_model import EmotionRecordInDb, EmotionRecordInTeam
from app.schemas.emotion_record_schema import EmotionRecord as EmotionRecordSchema

from app.utils.logger import logger


def create_emotion_record(db: Session, emotion_record: EmotionRecordModel):
    db_emotion_record = EmotionRecordSchema(
        emotion_id=emotion_record.emotion_id,
        intensity=emotion_record.intensity,
        notes=emotion_record.notes,
        is_anonymous=emotion_record.is_anonymous,
        user_id=emotion_record.user_id
    )
    db.add(db_emotion_record)
    db.commit()
    db.refresh(db_emotion_record)

    return db_emotion_record


def get_emotion_records_by_user_id(db: Session, users_id: list[int], for_team: bool = False, include_feedbacks: bool = False):
    emotion_records = db.query(EmotionRecordSchema).filter(EmotionRecordSchema.user_id.in_(users_id)).all()

    if for_team:
        result: list[EmotionRecordInTeam] = []
        for emotion_record in emotion_records:
            record = EmotionRecordInTeam(
                id=emotion_record.id,
                user_id=None if emotion_record.is_anonymous else emotion_record.user_id,
                emotion_id=emotion_record.emotion_id,
                intensity=emotion_record.intensity,
                notes=emotion_record.notes,
                is_anonymous=emotion_record.is_anonymous,
                user_name=None,  # Será preenchido posteriormente
                created_at=emotion_record.created_at
            )
            result.append(record)
    else:
        result: list[EmotionRecordInDb] = []
        for emotion_record in emotion_records:
            record = EmotionRecordInDb(
                id=emotion_record.id,
                user_id=None if emotion_record.is_anonymous else emotion_record.user_id,
                emotion_id=emotion_record.emotion_id,
                intensity=emotion_record.intensity,
                notes=emotion_record.notes,
                is_anonymous=emotion_record.is_anonymous,
                created_at=emotion_record.created_at,
                feedbacks=[]
            )
            
            # Se solicitado, incluir os feedbacks
            if include_feedbacks:
                from app.schemas.feedback_schema import Feedback
                from app.models.emotion_record_model import FeedbackSummary
                
                feedbacks = db.query(Feedback).filter(Feedback.emotion_record_id == emotion_record.id).all()
                for feedback in feedbacks:
                    feedback_summary = FeedbackSummary(
                        id=feedback.id,
                        message=feedback.message,
                        is_anonymous=feedback.is_anonymous,
                        created_at=feedback.created_at,
                        emotion_record_id=emotion_record.id
                    )
                    record.feedbacks.append(feedback_summary)
            
            result.append(record)

    return result


def get_emotion_records_by_user_id_and_emotion_id(db: Session, user_id: int, emotion_id: int, include_feedbacks: bool = False):
    emotion_records = db.query(EmotionRecordSchema).filter(EmotionRecordSchema.user_id == user_id,
                                                     EmotionRecordSchema.emotion_id == emotion_id).all()

    result: list[EmotionRecordInDb] = []
    for emotion_record in emotion_records:
        record = EmotionRecordInDb(
            id=emotion_record.id,
            user_id=None if emotion_record.is_anonymous else emotion_record.user_id,
            emotion_id=emotion_record.emotion_id,
            intensity=emotion_record.intensity,
            notes=emotion_record.notes,
            is_anonymous=emotion_record.is_anonymous,
            created_at=emotion_record.created_at,
            feedbacks=[]
        )
        
        # Se solicitado, incluir os feedbacks
        if include_feedbacks:
            from app.schemas.feedback_schema import Feedback
            from app.models.emotion_record_model import FeedbackSummary
            
            feedbacks = db.query(Feedback).filter(Feedback.emotion_record_id == emotion_record.id).all()
            for feedback in feedbacks:
                feedback_summary = FeedbackSummary(
                    id=feedback.id,
                    message=feedback.message,
                    is_anonymous=feedback.is_anonymous,
                    created_at=feedback.created_at,
                    emotion_record_id=emotion_record.id
                )
                record.feedbacks.append(feedback_summary)
        
        result.append(record)

    return result
