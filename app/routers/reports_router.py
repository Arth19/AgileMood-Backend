from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from datetime import date

from app.crud import reports_crud

from app.models.user_model import UserInDB
import app.models.reports_model as reports_model
from app.databases.sqlite_database import get_db

from app.routers.authentication import get_current_active_user
from app.utils.constants import Errors, Role
from app.utils.logger import logger

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

 
@router.get("/emoji-distribution/{team_id}", response_model=reports_model.EmojiDistributionReport)
def emoji_distribution(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    team_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to remove members from teams.")
        raise Errors.NO_PERMISSION

    response = reports_crud.get_emoji_distribution_report(db, team_id, start_date, end_date)

    return response


@router.get("/average-intensity/{team_id}", response_model=reports_model.AverageIntensityReport)
def average_intensity(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    team_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to remove members from teams.")
        raise Errors.NO_PERMISSION

    response = reports_crud.get_average_intensity_report(db, team_id, start_date, end_date)
    
    return response


@router.get("/user_emotion_analysis/{team_id}/{user_id}", response_model=reports_model.AnalysisByUser)
def get_emotion_analysis_by_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    team_id: int,
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to remove members from teams.")
        raise Errors.NO_PERMISSION

    response = reports_crud.get_emotion_analysis_by_user(db, team_id, user_id, start_date, end_date)
    
    return response



@router.get("/anonymous_records_emotion_analysis/{team_id}", response_model=reports_model.AnalysisByUser)
def get_anonymous_emotion_analysis(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    team_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):

    if current_user.role != Role.MANAGER:
        logger.error(f"User doesn't have the permission to remove members from teams.")
        raise Errors.NO_PERMISSION

    response = reports_crud.get_anonymous_emotion_analysis(db, team_id, start_date, end_date)
    
    return response
