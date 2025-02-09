from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import databases.sqlite_data_provider as db
from .user import User
from .emotion import Emotion


class EmotionRecord(db.Base):
    __tablename__ = "emotion_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emotion_id = Column(Integer, ForeignKey("emotions.id"), nullable=False)
    intensity = Column(String)
    notes = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="records")
    emotion = relationship("Emotion", back_populates="records")

