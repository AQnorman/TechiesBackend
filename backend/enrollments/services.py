import fastapi as _fastapi
import datetime as _dt
from auth import schemas as _UserSchema
from courses import schemas as _CourseSchema
from auth import models as _UserModel
from courses import models as _CourseModel
import sqlalchemy.orm as _orm
from dependencies import get_db
import json


async def add_user_to_course(db: _orm.Session, user_id: int, course_id: int):
    user_obj = db.query(_UserModel.User).filter(
        _UserModel.User.id == user_id).first()
    course_obj = db.query(_CourseModel.Course).filter(
        _CourseModel.Course.id == course_id).first()
    courses = user_obj.courses

    if course_obj not in courses:
        user_obj.id = user_id
        user_obj.email = user_obj.email
        user_obj.username = user_obj.username
        user_obj.is_active = user_obj.is_active
        user_obj.courses = user_obj.courses + [course_obj]

        db.commit()
        db.refresh(user_obj)

        return _UserSchema.User.from_orm(user_obj)

    raise _fastapi.HTTPException(
        status_code=403, detail="Course is already enrolled.")
