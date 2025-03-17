from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
import app.databases.sqlite_database as db

from app.utils.constants import DataBase


class Feedback(db.Base):
    __tablename__ = DataBase.FEEDBACK_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    emotion_record_id = Column(Integer, ForeignKey("emotion_record.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_anonymous = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    emotion_record = relationship("EmotionRecord")
    manager = relationship("User", foreign_keys=[manager_id]) 