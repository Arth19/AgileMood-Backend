from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum

# Enumeração para intensidade (1 a 5)
class IntensityEnum(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class EmotionRecord(BaseModel):
    user_id: int
    emotion_id: int
    intensity: IntensityEnum
    notes: str | None = None

    class Config:
        from_attributes = True


class EmotionRecordInDb(EmotionRecord):
    id:  int | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class AllEmotionReportsResponse(BaseModel):
    emotion_records: List[EmotionRecordInDb]
