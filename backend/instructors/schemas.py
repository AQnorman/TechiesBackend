import pydantic as _pydantic
from pydantic import BaseConfig

BaseConfig.arbitrary_types_allowed = True


class _InstructorBase(_pydantic.BaseModel):
    name: str
    about: str
    profession: str


class InstructorCreate(_InstructorBase):
    pass


class Instructor(_InstructorBase):
    id: int

    class Config:
        orm_mode = True
