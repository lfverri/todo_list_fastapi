from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserList(BaseModel):
    users: list[UserPublic]
