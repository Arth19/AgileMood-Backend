from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from app.schemas.team_schema import Team, user_teams
from app.schemas.user_schema import User

from app.crud.user_crud import get_user_by_id
from app.crud.emotion_record_crud import get_emotion_records_by_user_id

from app.models.team_model import Team as TeamModel
from app.models.emotion_record_model import EmotionRecordInTeam

from app.utils.logger import logger


def create_team(db: Session, name: str, manager_id: int):
    """
    Creates a new team in the database.
    """
    db_team = Team(
        name=name,
        manager_id=manager_id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_id(db: Session, team_id: int):
    """
    Returns a team by ID
    """
    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return None  # 🔥 Retorna None caso o time não exista

    # Obtém os registros de emoção dos membros do time
    member_ids = [user.id for user in team.members]
    emotions_records: list[EmotionRecordInTeam] = get_emotion_records_by_user_id(db, member_ids, for_team=True)

    # Evita o erro de índice verificando o tamanho das listas antes de atribuir
    for i in range(min(len(emotions_records), len(team.members))):
        emotions_records[i].user_name = team.members[i].name

    # Retorna os dados do time corretamente
    team_data = {
        "team_data": team,
        "members": team.members,
        "emotions_reports": emotions_records
    }

    return team_data


def get_all_teams(db: Session, manager_id: int):
    """
    Return all created teams in the database
    """

    return db.query(Team).filter(Team.manager_id == manager_id).all()
    # result = []

    # for team in all_teams:
    #     result.append(db.query(Team).filter(Team.id.is_(team.id)).first())
        
    # return result


def update_team(db: Session, team_id: int, team_update: TeamModel):
    """
    Updates an existing team by ID
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    team_data = {
        "team_data": db_team,
        "members": db.query(User).join(user_teams).filter(user_teams.c.team_id == team_id).all(),
    }
    
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return None

    for key, value in team_update.dict().items():
        if hasattr(db_team, key):
            setattr(db_team, key, value)

    db.commit()
    db.refresh(db_team)
    logger.debug(f"Team with ID {team_id} was updated successfully.")
    
    return team_data


def delete_team(db: Session, team_id: int):
    """
    Deletes a team by ID
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return False

    db.delete(db_team)
    db.commit()
    logger.debug(f"Team with ID {team_id} was deleted successfully.")
    return True


def add_team_member(db: Session, team_id: int, user_id: int):
    if not _validate_team_and_user_existence(db, team_id, user_id):
        return None

    existing_user_team = db.query(user_teams).filter_by(user_id=user_id, team_id=team_id).first()
    if existing_user_team:
        logger.error(f"User with ID {user_id} is already a member of the team that has ID {team_id}")
        return None

    db.execute(insert(user_teams).values(user_id=user_id, team_id=team_id))
    db.commit()
    
    return get_team_by_id(db, team_id)


def remove_team_member(db: Session, team_id: int, user_id: int):
    if not _validate_team_and_user_existence(db, team_id, user_id):
        logger.error(f"Team with ID:= {team_id} doesn't exist")
        return None

    existing_user_team = db.query(user_teams).filter_by(user_id=user_id, team_id=team_id).first()
    if not existing_user_team:
        logger.error(f"User with ID:= {user_id} doesn't belong to the team that has ID {team_id}")
        return None

    db.execute(
        delete(user_teams).where(user_teams.c.user_id == user_id, user_teams.c.team_id == team_id)
    )
    db.commit()
    
    return get_team_by_id(db, team_id)


def is_manager_of_team(db: Session, user_id: int, team_id: int) -> bool:
    """
    Verifies if the user is the team's manager
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    return team is not None and team.manager_id == user_id


def _validate_team_and_user_existence(db: Session, team_id: int, user_id: int) -> bool:
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return False

    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        logger.error(f"User with ID {user_id} not found.")
        return False

    return True
