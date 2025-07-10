from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

from app.models.emotion_model import EmotionInDb

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


class FeedbackSummary(BaseModel):
    id: int
    message: str
    is_anonymous: bool
    created_at: datetime
    emotion_record_id: int
    
    class Config:
        from_attributes = True


class EmotionRecordInDb(EmotionRecord):
    # O ID é essencial para identificar unicamente cada registro de emoção
    # e permitir operações como envio de feedback e filtragem por data
    id:  int | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    feedbacks: List[FeedbackSummary] = []


class EmotionRecordWithEmotion(EmotionRecordInDb):
    """Emotion record with the associated Emotion data."""
    emotion: EmotionInDb


class AllEmotionReportsResponse(BaseModel):
    emotion_records: List[EmotionRecordInDb]


class EmotionRecordInTeam(EmotionRecord):
    # O ID é essencial para identificar unicamente cada registro de emoção
    # e permitir operações como envio de feedback e filtragem por data
    id: int | None = None
    user_name: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
