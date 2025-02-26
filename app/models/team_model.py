from pydantic import BaseModel, Field
from datetime import datetime
from app.models.user_model import UserInTeam
from app.models.emotion_record_model import EmotionRecordInDb
from app.models.emotion_model import EmotionInDb
from typing import List


class Team(BaseModel):
    name: str

    class Config:
        from_attributes = True


class TeamData(Team):
    id: int
    manager_id: int | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class TeamResponse(BaseModel):
    team_data: TeamData
    members: List[UserInTeam]
    emotions_reports: List[EmotionRecordInDb]
    emotions: List[EmotionInDb]


class AllTeamsResponse(BaseModel):
    teams: List[TeamData]


# class Team(BaseModel):
#     name: str

#     class Config:
#         from_attributes = True


# class TeamCreate(Team):
#     manager_id: int | None = None


# class TeamData(TeamCreate):
#     id: int
#     created_at: datetime = Field(default_factory=datetime.now)

#     class Config:
#         from_attributes = True