from pydantic import BaseModel
from typing import List


class EmojiDistribution(BaseModel):
    emoji: str
    emotion_name: str
    frequency: int


class AverageIntensity(BaseModel):
    emoji: str
    emotion_name: str
    avg_intensity: float


class EmotionAvgAndFrequency(EmojiDistribution):
    avg_intensity: float


class AnalysisByUser(BaseModel):
    user_name: str
    all_user_emotion_records: List[EmotionAvgAndFrequency]

    