from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
import app.databases.sqlite_database as db

from app.utils.constants import DataBase


# Tabela Emotion
class Emotion(db.Base):
    __tablename__ = DataBase.EMOTION_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    emoji = Column(String, nullable=True)
    color = Column(String, nullable=True)
    

# Tabela EmotionRecord
class EmotionRecord(db.Base):
    __tablename__ = DataBase.EMOTION_RECORDS_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # Chave estrangeira para User
    emotion_id = Column(Integer, ForeignKey("emotion.id"), nullable=False)  # Chave estrangeira para Emotion
    intensity = Column(Integer, nullable=False)  # Intensidade entre 1 e 5
    notes = Column(String, nullable=True)  # Notas opcionais
    timestamp = Column(DateTime, default=datetime.datetime.now)  # Timestamp automático

    # Relacionamentos
    user = relationship("User", back_populates="emotion_records")
    emotion = relationship("Emotion")