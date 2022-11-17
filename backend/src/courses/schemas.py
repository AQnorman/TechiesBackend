from typing import List
import datetime as _dt
import pydantic as _pydantic
from pydantic import BaseConfig

BaseConfig.arbitrary_types_allowed = True


# COURSE
class _CourseBase(_pydantic.BaseModel):
    name: str
    desc: str
    outline: str
    outcomes: str
    duration: str
    start_date: _dt.datetime
    fees: int


class CourseCreate(_CourseBase):
    pass

    class Config:
        orm_mode = True


class Course(_CourseBase):
    id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True
