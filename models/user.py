from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import databases.sqlite_data_provider as db


class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    records = relationship("EmotionRecord", back_populates="user")
