from typing import Optional
import pydantic as _pydantic
from pydantic import BaseConfig
from courses import schemas as _CourseSchema

BaseConfig.arbitrary_types_allowed = True


class _UserBase(_pydantic.BaseModel):
    username: str
    email: str
    phone: int


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserAuth(_UserBase):
    hashed_password: str
    id: int

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    is_active: bool
    courses: list[_CourseSchema.Course] = []

    class Config:
        orm_mode = True
