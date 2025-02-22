from pydantic import BaseModel
from typing import List


class Emotion(BaseModel):
    name: str
    emoji: str | None = None
    color: str | None = None
    team_id: int | None = None
    is_negative: bool

    class Config:
        from_attributes = True


class EmotionInDb(Emotion):
    id: int | None = None


class EmotionUpdate(BaseModel):
    name: str = None
    emoji: str | None = None
    color: str | None = None
    is_negative: bool


class AllEmotionsResponse(BaseModel):
    emotions: List[EmotionInDb]
