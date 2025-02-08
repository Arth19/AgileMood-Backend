from sqlalchemy import Column, Integer, String

import databases.sqlite_data_provider as db


class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
