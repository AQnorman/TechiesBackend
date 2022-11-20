import pydantic as _pydantic
from pydantic import BaseConfig
from auth import schemas as _UserSchema
import datetime as _dt

BaseConfig.arbitrary_types_allowed = True


class _FeedbackBase(_pydantic.BaseModel):
    feedback: str


class FeedbackCreate(_FeedbackBase):
    pass


class Feedback(_FeedbackBase):
    id: int
    student: _UserSchema.User
    date_created: _dt.datetime
    date_last_updated = _dt.datetime

    class Config:
        orm_mode = True
