from typing import Optional
from enum import Enum
import pydantic as _pydantic
from pydantic import BaseConfig
from courses import schemas as _CourseSchema

BaseConfig.arbitrary_types_allowed = True


class _UserBase(_pydantic.BaseModel):
    username: str
    email: str
    phone: int


class _AdminBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class AdminCreate(_AdminBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserAuth(_UserBase):
    hashed_password: str
    id: int

    class Config:
        orm_mode = True


class AdminAuth(_AdminBase):
    hashed_password: str
    id: int

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    is_active: bool
    role: str
    courses: list[_CourseSchema.Course] = []

    class Config:
        orm_mode = True


class Admin(_AdminBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True
