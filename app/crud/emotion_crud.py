from sqlalchemy.orm import Session

from app.schemas.emotion_record_schema import Emotion
from app.crud.team_crud import is_manager_of_team
from app.schemas.team_schema import Team
from app.utils.logger import logger


def create_emotion(db: Session, emotion: Emotion, user_id: int):

    db_team = db.query(Team).filter(Team.id == emotion.team_id).first()

    if not is_manager_of_team(db, user_id, emotion.team_id):
        logger.error(f"User with ID {user_id} isn't the Team manager where Team's ID is {emotion.team_id}.")
        return None

    if db_team is None:
        logger.error(f"Team with ID {emotion.team_id} not found.")
        return None
    
    db_emotion = Emotion(
        name=emotion.name,
        emoji=emotion.emoji,
        color=emotion.color,
        team_id=emotion.team_id
    )
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)

    return db_emotion


def get_emotion_by_id(db: Session, emotion_id: int, user_id: int):
    db_emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if db_emotion is None:
        logger.error(f"Emotion with ID {emotion_id} not found.")
        return None

    if not is_manager_of_team(db, user_id, db_emotion.team_id):
        logger.error(f"User with ID {user_id} isn't the Team manager where Team's ID is {db_emotion.team_id}.")
        return None

    return db_emotion


def get_all_emotions(db: Session, user_id: int):
    managed_teams = db.query(Team).filter(Team.manager_id == user_id).all()
    if not managed_teams:
        logger.error(f"User with ID {user_id} isn't a manager of any existing team.")
        return None

    # Busca todas as Emotions desses times
    team_ids = [team.id for team in managed_teams]
    return db.query(Emotion).filter(Emotion.team_id.in_(team_ids)).all()


def update_emotion(db: Session, emotion_id: int, emotion_update: dict, user_id: int):
    """
    Updates an Emotion if the user is the team manager
    """
    db_emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if db_emotion is None:
        logger.error(f"Emotion with ID {emotion_id} not found.")
        return None

    if not is_manager_of_team(db, user_id, db_emotion.team_id):
        logger.error(f"User with ID {user_id} isn't the Team manager where Team's ID is{db_emotion.team_id}.")
        return None

    for key, value in emotion_update.items():
        if hasattr(db_emotion, key):
            setattr(db_emotion, key, value)

    db.commit()
    db.refresh(db_emotion)

    logger.debug(f"Emotion with ID {emotion_id} updated successfully.")
    return db_emotion


def delete_emotion(db: Session, emotion_id: int, user_id: int):
    """
    Deletes an Emotion if the user is the team manager.
    """
    db_emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if db_emotion is None:
        logger.error(f"Emotion with ID {emotion_id} not found.")
        return False

    if not is_manager_of_team(db, user_id, db_emotion.team_id):
        logger.error(f"User with ID {user_id} isn't the Team manager where Team's ID is{db_emotion.team_id}.")
        return False

    db.delete(db_emotion)
    db.commit()

    logger.debug(f"Emotion with ID {emotion_id} deleted successfully.")
    return True


def get_emotions_by_team(db: Session, team_id: int, user_id: int):
    """
    Returns all Emotions from a Team if the user is its manager.
    """
    if not is_manager_of_team(db, user_id, team_id):
        logger.error(f"User with ID {user_id} isn't the Team manager where Team's ID is{team_id}.")
        return None

    return db.query(Emotion).filter(Emotion.team_id == team_id).all()