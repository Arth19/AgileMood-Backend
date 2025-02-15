from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
import app.databases.sqlite_database as db

from app.utils.constants import DataBase


class Emotion(db.Base):
    __tablename__ = DataBase.EMOTION_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    emoji = Column(String, nullable=True)
    color = Column(String, nullable=True)
    

class EmotionRecord(db.Base):
    __tablename__ = DataBase.EMOTION_RECORDS_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False) 
    emotion_id = Column(Integer, ForeignKey("emotion.id"), nullable=False)
    intensity = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="emotion_records")
    emotion = relationship("Emotion")