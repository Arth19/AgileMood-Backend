from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
    name: str
    email: str
    disabled: bool | None = False
    role: Literal["manager", "employee"] = Field(default="employee", description="User role in the organization")


class UserCreate(User):
    password: str


class UserInDB(User):
    id: int | None = None
    hashed_password: str