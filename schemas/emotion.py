from pydantic import BaseModel
from typing import Optional


class Emotion(BaseModel):
    id: str
    name: str
    icon: Optional[str] = None  # Ícone é opcional
    color: Optional[str] = None  # Cor é opcional

    class Config:
        from_attributes = True