import fastapi as _fastapi
import datetime as _dt
from ..auth import schemas as _UserSchema
from . import schemas as _CourseSchema
import sqlalchemy.orm as _orm
from ..dependencies import get_db
from . import models as _models


async def create_course(course: _CourseSchema.Course, db: _orm.Session):
    exists = db.query(_models.Course).filter(
        _models.Course.name == course.name).first()
    if exists is None:
        course = _models.Course(**course.dict())
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    raise _fastapi.HTTPException(
        status_code=403, detail="Course Already Exists.")


async def get_courses(db: _orm.Session):
    courses = db.query(_models.Course)
    return list(map(_CourseSchema.Course.from_orm, courses))


async def _course_selector(course_id: int, db: _orm.Session):
    course = (
        db.query(_models.Course)
        .filter(_models.Course.id == course_id)
        .first()
    )

    if course is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Course not Found.")

    return course


async def get_course(course_id: int, db: _orm.Session):
    course = await _course_selector(course_id=course_id, db=db)

    return _CourseSchema.Course.from_orm(course)


async def delete_course(course_id: int, db: _orm.Session):
    course = await _course_selector(course_id=course_id, db=db)

    db.delete(course)
    db.commit()


async def update_course(course_id: int, course: _CourseSchema.Course, db: _orm.Session):
    course_db = await _course_selector(course_id=course_id, db=db)

    course_db.name = course.name
    course_db.desc = course.desc
    course_db.outline = course.outline
    course_db.outcomes = course.outcomes
    course_db.duration = course.duration
    course_db.start_date = course.start_date
    course_db.fees = course.fees
    course_db.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(course_db)

    return _CourseSchema.Course.from_orm(course_db)
