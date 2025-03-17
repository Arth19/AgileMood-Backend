from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class FeedbackBase(BaseModel):
    message: str
    emotion_record_id: int
    is_anonymous: bool = False
    
    class Config:
        from_attributes = True


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackInDb(FeedbackBase):
    id: int
    manager_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True


class FeedbackResponse(FeedbackInDb):
    manager_knows_identity: bool = False


class AllFeedbacksResponse(BaseModel):
    feedbacks: List[FeedbackResponse] 