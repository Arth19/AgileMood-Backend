from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum


class IntensityEnum(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class EmotionRecord(BaseModel):
    user_id: int | None = None
    emotion_id: int
    intensity: IntensityEnum
    notes: str | None = None
    is_anonymous: bool | None = False
    
    class Config:
        from_attributes = True


class EmotionRecordInDb(EmotionRecord):
    id:  int | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class AllEmotionReportsResponse(BaseModel):
    emotion_records: List[EmotionRecordInDb]


class EmotionRecordInTeam(EmotionRecord):
    user_name:  str | None = None
