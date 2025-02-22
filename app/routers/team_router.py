from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.models.team_model import Team, TeamResponse, AllTeamsResponse, TeamData
from app.models.user_model import UserInDB
from app.models.emotion_model import AllEmotionsResponse
from app.databases.sqlite_database import get_db
from app.utils.constants import Errors, Role
from app.utils.logger import logger
from app.crud import team_crud
from app.crud import emotion_crud
from app.routers.authentication import get_current_active_user

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.post("/", response_model=TeamData)
def create_team(
        team: Team,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Creates a new team.
    Only users with the 'manager' role can create new teams.
    """
    logger.debug("Call to create a new team.")

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to create new teams.")
        raise Errors.NO_PERMISSION

    team.manager_id = current_user.id
    
    db_team = team_crud.create_team(db, team)
    if db_team is None:
        raise Errors.INVALID_PARAMS

    return db_team


@router.get("/{team_id}", response_model=TeamResponse)
def get_team_by_id(
        team_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Returns a Team by its ID.
    """
    logger.debug(f"Call to get the Team with ID: {team_id}")

    team = team_crud.get_team_by_id(db, team_id)
    if team is None:
        logger.error(f"Team with ID {team_id} not found.")
        raise Errors.NOT_FOUND

    return team


@router.get("/", response_model=AllTeamsResponse)
def get_all_teams(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Returns all the created Teams.
    """
    logger.debug("Call to list all created Teams.")

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION

    teams = team_crud.get_all_teams(db)
    if not teams:
        logger.error("There no teams in our database.")

    return AllTeamsResponse(teams=teams)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
        team_id: int,
        team_update: Team,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Updates one existing team.
    Only users with the 'manager' role can update teams.
    """
    logger.debug(f"Call to update the Team with ID: {team_id}")

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to update teams.")
        raise Errors.NO_PERMISSION

    team_update.manager_id = current_user.id
    db_team = team_crud.update_team(db, team_id, team_update)
    if db_team is None:
        logger.error(f"Failed to update team with ID: {team_id}")
        raise Errors.NOT_FOUND

    return db_team


@router.delete("/{team_id}")
def delete_team(
        team_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Deletes a team by ID.
    Only users with the 'manager' role can delete teams.
    """
    logger.debug(f"Call to delete the Team with ID: {team_id}")

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to delete teams.")
        raise Errors.NO_PERMISSION

    success = team_crud.delete_team(db, team_id)
    if not success:
        logger.error(f"Team with ID {team_id} not found.")
        raise Errors.NOT_FOUND

    return {"message": f"Team with ID {team_id} successfully deleted."}


@router.post("/{team_id}/{user_id}", response_model=TeamResponse)
def add_team_member(
        team_id: int,
        user_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Adds a new member to a team.
    Only users with the 'manager' role can add a new member to a team.
    """
    logger.debug("Call to add a new member to a team.")

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to add new members to a team.")
        raise Errors.NO_PERMISSION
    
    db_team = team_crud.add_team_member(db, team_id, user_id)
    if db_team is None:
        raise Errors.INVALID_PARAMS

    return db_team


@router.delete("/{team_id}/{user_id}", response_model=TeamResponse)
def remove_team_member(
        team_id: int,
        user_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Remove a member from a team.
    Only users with the 'manager' role can remove members from teams.
    """
    logger.debug("Call to remove a member from a team.")

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to remove members from teams.")
        raise Errors.NO_PERMISSION
    
    db_team = team_crud.remove_team_member(db, team_id, user_id)
    if db_team is None:
        raise Errors.INVALID_PARAMS

    return db_team


@router.get("/{team_id}/emotions", response_model=AllEmotionsResponse)
def get_emotions_by_team(
        team_id: int,
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    """
    Returns all Emotions from a Team, if the user is the Team's manager.
    """
    logger.debug(f"Call to list all Emotions from the Team with ID: {team_id}")

    if current_user.role != Role.MANAGER:
        raise Errors.NO_PERMISSION

    emotions = emotion_crud.get_emotions_by_team(db, team_id, current_user.id)
    if emotions is None:
        raise Errors.NO_PERMISSION

    return AllEmotionsResponse(emotions=emotions)
