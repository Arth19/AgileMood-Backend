from pydantic import BaseModel
from typing import List


class Emotion(BaseModel):
    name: str
    emoji: str | None = None
    color: str | None = None

    class Config:
        from_attributes = True  # Para compatibilidade com ORMs como SQLAlchemy


class EmotionInDb(Emotion):
    id: int | None = None


class EmotionUpdate(BaseModel):
    name: str = None
    emoji: str | None = None
    color: str | None = None


class EmotionsResponse(BaseModel):
    emotions: List[EmotionInDb]
