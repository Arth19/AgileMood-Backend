from pydantic import BaseModel
from typing import List


class EmotionsResponse(BaseModel):
    emotions: List[str]
