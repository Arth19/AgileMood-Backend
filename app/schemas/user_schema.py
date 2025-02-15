from sqlalchemy import Column, Integer, String, Boolean
import app.databases.sqlite_database as db
from sqlalchemy.orm import relationship
import enum

from app.utils.constants import DataBase

# Defina uma enumeração para os papéis (roles)
class RoleEnum(str, enum.Enum):
    MANAGER = "manager"
    EMPLOYEE = "employee"


class User(db.Base):
    __tablename__ = DataBase.USER_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=RoleEnum.EMPLOYEE.value)

    # Relacionamento com EmotionRecord
    emotion_records = relationship("EmotionRecord", back_populates="user")
    