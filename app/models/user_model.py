from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    name: str
    email: str
    disabled: bool | None = None


class UserCreate(User):
    password: str


class UserInDB(User):
    hashed_password: str
