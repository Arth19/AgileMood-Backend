from pydantic import BaseModel
from datetime import datetime
from typing import List


class EmotionRecord(BaseModel):
    id: int | None = None
    user_id: int | None = None
    emotion: str  # emotion
    intensity: int  # intensity between 1 and 5
    notes: str | None = None  # Additional notes (optional)
    timestamp: datetime = datetime.now()  # timestamp

    class Config:
        from_attributes = True


class AllEmotionReportsResponse(BaseModel):
    reports: List[EmotionRecord]
