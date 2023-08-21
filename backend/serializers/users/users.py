from pydantic import BaseModel

from backend.custom_base_model import PydanticBaseModel
from backend.models import User


class UserCreateValidator(PydanticBaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True
        db_model = User


class UserGetValidator(PydanticBaseModel):
    user_uui: str
    name: str
    password: str
    is_admin: bool

    class Config:
        orm_mode = True
        db_model = User
