from typing import Optional
import datetime as _dt
import pydantic as _pydantic
from pydantic import BaseConfig
from instructors import schemas as _InstructorSchema


# COURSE
class _CourseBase(_pydantic.BaseModel):
    name: str
    desc: str
    outline: str
    outcomes: str
    duration: str
    start_date: _dt.date
    fees: int


class CourseCreate(_CourseBase):
    pass


class Course(_CourseBase):
    id: int
    instructor: _InstructorSchema.Instructor
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True
