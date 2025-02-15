from sqlalchemy import delete, insert
from sqlalchemy.orm import Session
from app.schemas.team_schema import Team, user_teams
from app.schemas.user_schema import User
from app.crud.user_crud import get_user_by_id
from app.models.team_model import Team as TeamModel
from app.utils.logger import logger

def create_team(db: Session, team: Team):
    """
    Creates a new team in the database.
    """
    db_team = Team(
        name=team.name,
        manager_id=team.manager_id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_id(db: Session, team_id: int):
    """
    Returns a team by it's ID
    """

    teamData = {
        "team_data": db.query(Team).filter(Team.id == team_id).first(),
        "members": db.query(User).join(user_teams).filter(user_teams.c.team_id == team_id).all(),
        }
    
    return teamData


def get_all_teams(db: Session):
    """
    Return all created teams in the database
    """
    return db.query(Team).all()


def update_team(db: Session, team_id: int, team_update: TeamModel):
    """
    Updates a existing team by it's ID
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return None

    for key, value in team_update.dict().items():
        if hasattr(db_team, key):
            setattr(db_team, key, value)

    db.commit()
    db.refresh(db_team)
    logger.debug(f"Team with ID {team_id} was updated successfully.")
    return db_team


def delete_team(db: Session, team_id: int):
    """
    Deletes a team by it's ID
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return False

    db.delete(db_team)
    db.commit()
    logger.debug(f"Team with ID {team_id} was deleted sucessfully.")
    return True


def add_team_member(db: Session, team_id: int, user_id: int):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    db_user = get_user_by_id(db, user_id)
    
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return None

    if db_user is None:
        logger.error(f"User with ID {user_id} not found.")
        return None

    existing_user_team = db.query(user_teams).filter_by(user_id=user_id, team_id=team_id).first()
    if existing_user_team:
        logger.error(f"User with ID {user_id} is already a member of the team that has ID {team_id}")
        return None

    db.execute(
        insert(user_teams).values(user_id=user_id, team_id=team_id)
    )
    db.commit()
    
    return get_team_by_id(db, team_id)


def remove_team_member(db: Session, team_id: int, user_id: int):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    db_user = get_user_by_id(db, user_id)
    
    if db_team is None:
        logger.error(f"Team with ID {team_id} not found.")
        return None

    if db_user is None:
        logger.error(f"User with ID {user_id} not found.")
        return None

    existing_user_team = db.query(user_teams).filter_by(user_id=user_id, team_id=team_id).first()
    if not existing_user_team:
        logger.error(f"User with ID:= {user_id} doesn't belong to the team that has ID {team_id}")
        return None

    db.execute(
        delete(user_teams).where(user_teams.c.user_id==user_id, user_teams.c.team_id==team_id)
    )
    db.commit()
    
    return get_team_by_id(db, team_id)


def is_manager_of_team(db: Session, user_id: int, team_id: int) -> bool:
    """
    Verifies if the user is the team's manager
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    return team is not None and team.manager_id == user_id