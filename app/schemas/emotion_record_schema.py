from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class EmotionRecordCreate(BaseModel):
    user_id: int  # user identifier
    emotion: str  # emotion
    intensity: int  # intensity between 1 and 5
    notes: Optional[str] = None  # Additional notes (optional)
    timestamp: datetime = datetime.now()  # timestamp

    class Config:
        from_attributes = True


class EmotionRecordResponse(BaseModel):
    id: int
    user_id: int
    emotion: str
    intensity: int
    notes: Optional[str] = None


class AllEmotionReportsResponse(BaseModel):
    reports: List[EmotionRecordResponse]
