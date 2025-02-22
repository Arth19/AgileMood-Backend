from pydantic import BaseModel
from typing import List


class EmojiDistribution(BaseModel):
    emotion_name: str
    frequency: int


class EmojiDistributionReport(BaseModel):
    emoji_distribution: List[EmojiDistribution]
    negative_emotion_ratio: float
    alert: str | None = None


class AverageIntensity(BaseModel):
    emotion_name: str
    avg_intensity: float


class AverageIntensityReport(BaseModel):
    average_intensity: List[AverageIntensity]
    negative_emotion_ratio: float
    alert: str | None = None


class EmotionAvgAndFrequency(EmojiDistribution):
    avg_intensity: float


class AnalysisByUser(BaseModel):
    user_name: str
    all_user_emotion_records: List[EmotionAvgAndFrequency]

    