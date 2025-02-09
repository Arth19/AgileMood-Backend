from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import databases.sqlite_data_provider as db


class Emotion(db.Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)

    records = relationship("EmotionRecord", back_populates="emotion")