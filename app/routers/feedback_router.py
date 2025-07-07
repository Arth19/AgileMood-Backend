from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.crud import feedback_crud
from app.crud import emotion_record_crud

from app.models.feedback_model import FeedbackCreate, FeedbackResponse, AllFeedbacksResponse
from app.models.user_model import UserInDB

from app.routers.authentication import get_current_active_user

from app.databases.postgres_database import get_db

from app.utils.constants import Errors, Role
from app.utils.logger import logger


router = APIRouter(
    prefix="/feedback",
    tags=["feedbacks"],
)


@router.post("/", response_model=FeedbackResponse)
def create_feedback(
        feedback: FeedbackCreate,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Cria um novo feedback para um registro de emoção.
    Apenas gerentes podem criar feedbacks.
    """
    logger.debug("call to create feedback")

    # Verificar se o usuário é um gerente
    if current_user.role != Role.MANAGER:
        logger.error(f"User {current_user.id} is not a manager")
        raise Errors.NO_PERMISSION

    # Verificar se o gerente pode enviar feedback para este registro de emoção
    can_send = feedback_crud.can_manager_send_feedback(db, current_user.id, feedback.emotion_record_id)
    if not can_send:
        logger.error(f"Manager {current_user.id} cannot send feedback to emotion record {feedback.emotion_record_id}")
        raise Errors.NO_PERMISSION

    # Criar o feedback
    db_feedback = feedback_crud.create_feedback(db, feedback, current_user.id)
    if db_feedback is None:
        raise Errors.INVALID_PARAMS

    # Buscar o registro de emoção para verificar se é anônimo
    emotion_record = db.query(emotion_record_crud.EmotionRecordSchema).filter(
        emotion_record_crud.EmotionRecordSchema.id == feedback.emotion_record_id
    ).first()

    # Converter para o modelo de resposta
    response = FeedbackResponse(
        id=db_feedback.id,
        message=db_feedback.message,
        emotion_record_id=db_feedback.emotion_record_id,
        manager_id=db_feedback.manager_id,
        is_anonymous=db_feedback.is_anonymous,
        created_at=db_feedback.created_at,
        manager_knows_identity=not emotion_record.is_anonymous
    )

    return response


@router.get("/", response_model=AllFeedbacksResponse)
def get_feedbacks_for_current_user(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Retorna todos os feedbacks recebidos pelo usuário atual.
    """
    logger.debug("call to get feedbacks for current user")

    feedbacks = feedback_crud.get_feedbacks_by_user_id(db, current_user.id)
    return AllFeedbacksResponse(feedbacks=feedbacks)


@router.get("/emotion-record/{emotion_record_id}", response_model=AllFeedbacksResponse)
def get_feedbacks_by_emotion_record(
        emotion_record_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Retorna todos os feedbacks para um registro de emoção específico.
    O usuário só pode ver feedbacks para seus próprios registros de emoção.
    """
    logger.debug(f"call to get feedbacks for emotion record {emotion_record_id}")

    # Verificar se o registro de emoção pertence ao usuário
    emotion_record = db.query(emotion_record_crud.EmotionRecordSchema).filter(
        emotion_record_crud.EmotionRecordSchema.id == emotion_record_id
    ).first()

    if not emotion_record:
        logger.error(f"Emotion record {emotion_record_id} not found")
        raise Errors.NOT_FOUND

    if emotion_record.user_id != current_user.id and current_user.role != Role.MANAGER:
        logger.error(f"User {current_user.id} cannot access emotion record {emotion_record_id}")
        raise Errors.NO_PERMISSION

    feedbacks = feedback_crud.get_feedbacks_by_emotion_record_id(db, emotion_record_id)
    
    # Converter para o modelo de resposta
    result = []
    for feedback in feedbacks:
        feedback_response = FeedbackResponse(
            id=feedback.id,
            message=feedback.message,
            emotion_record_id=feedback.emotion_record_id,
            manager_id=feedback.manager_id,
            is_anonymous=feedback.is_anonymous,
            created_at=feedback.created_at,
            manager_knows_identity=not emotion_record.is_anonymous
        )
        result.append(feedback_response)
    
    return AllFeedbacksResponse(feedbacks=result) 