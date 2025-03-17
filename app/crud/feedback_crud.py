from sqlalchemy.orm import Session

from app.models.feedback_model import FeedbackCreate, FeedbackResponse
from app.schemas.feedback_schema import Feedback
from app.schemas.emotion_record_schema import EmotionRecord
from app.crud.team_crud import is_manager_of_team

from app.utils.logger import logger


def create_feedback(db: Session, feedback: FeedbackCreate, manager_id: int):
    # Verificar se o registro de emoção existe
    emotion_record = db.query(EmotionRecord).filter(EmotionRecord.id == feedback.emotion_record_id).first()
    if not emotion_record:
        logger.error(f"Emotion record with ID {feedback.emotion_record_id} not found")
        return None
    
    # Criar o feedback
    db_feedback = Feedback(
        message=feedback.message,
        emotion_record_id=feedback.emotion_record_id,
        manager_id=manager_id,
        is_anonymous=feedback.is_anonymous
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback


def get_feedbacks_by_emotion_record_id(db: Session, emotion_record_id: int):
    return db.query(Feedback).filter(Feedback.emotion_record_id == emotion_record_id).all()


def get_feedbacks_by_user_id(db: Session, user_id: int):
    # Buscar todos os registros de emoção do usuário
    emotion_records = db.query(EmotionRecord).filter(EmotionRecord.user_id == user_id).all()
    
    if not emotion_records:
        return []
    
    # Buscar todos os feedbacks associados a esses registros
    emotion_record_ids = [record.id for record in emotion_records]
    feedbacks = db.query(Feedback).filter(Feedback.emotion_record_id.in_(emotion_record_ids)).all()
    
    # Converter para o modelo de resposta
    result = []
    for feedback in feedbacks:
        # Verificar se o feedback é anônimo
        emotion_record = db.query(EmotionRecord).filter(EmotionRecord.id == feedback.emotion_record_id).first()
        
        # Se o feedback for anônimo, o gerente não sabe a identidade do colaborador
        manager_knows_identity = not emotion_record.is_anonymous
        
        feedback_response = FeedbackResponse(
            id=feedback.id,
            message=feedback.message,
            emotion_record_id=feedback.emotion_record_id,
            manager_id=feedback.manager_id,
            is_anonymous=feedback.is_anonymous,
            created_at=feedback.created_at,
            manager_knows_identity=manager_knows_identity
        )
        result.append(feedback_response)
    
    return result


def can_manager_send_feedback(db: Session, manager_id: int, emotion_record_id: int):
    """
    Verifica se o gerente pode enviar feedback para um registro de emoção específico
    """
    # Buscar o registro de emoção
    emotion_record = db.query(EmotionRecord).filter(EmotionRecord.id == emotion_record_id).first()
    if not emotion_record:
        return False
    
    # Se o registro for anônimo, o gerente pode enviar feedback sem saber quem é o colaborador
    if emotion_record.is_anonymous:
        # Mas ainda precisamos verificar se o gerente é gerente do time do colaborador
        # Para isso, precisamos buscar o time do colaborador
        from app.schemas.user_schema import User
        from app.schemas.team_schema import Team, user_teams
        
        user = db.query(User).filter(User.id == emotion_record.user_id).first()
        if not user:
            return False
        
        # Buscar os times do usuário
        teams = db.query(Team).join(user_teams).filter(user_teams.c.user_id == user.id).all()
        
        # Verificar se o gerente é gerente de algum dos times
        for team in teams:
            if team.manager_id == manager_id:
                return True
        
        return False
    else:
        # Se o registro não for anônimo, o gerente precisa ser gerente do time do colaborador
        user_id = emotion_record.user_id
        
        # Buscar os times do usuário
        from app.schemas.user_schema import User
        from app.schemas.team_schema import Team, user_teams
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Buscar os times do usuário
        teams = db.query(Team).join(user_teams).filter(user_teams.c.user_id == user.id).all()
        
        # Verificar se o gerente é gerente de algum dos times
        for team in teams:
            if team.manager_id == manager_id:
                return True
        
        return False 