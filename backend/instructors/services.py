import fastapi as _fastapi
from . import models as _models
from . import schemas as _schemas
from dependencies import get_db
import sqlalchemy.orm as _orm


async def create_instructor(instructor: _schemas.InstructorCreate, db: _orm.Session):
    exists = db.query(_models.Instructor).filter(
        _models.Instructor.name == instructor.name
    ).first()

    if exists is None:
        instructor = _models.Instructor(**instructor.dict())
        db.add(instructor)
        db.commit()
        db.refresh(instructor)
        return instructor

    raise _fastapi.HTTPException(
        status_code=403, detail="Instructor Already Exists."
    )


async def get_instructors(db: _orm.Session):
    instructors = db.query(_models.Instructor)
    return list(map(_schemas.Instructor.from_orm, instructors))


async def _instructor_selector(instructor_id: int, db: _orm.Session):
    instructor = db.query(_models.Instructor).filter(
        _models.Instructor.id == instructor_id).first()

    if instructor is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Instructor Not Found."
        )

    return instructor


async def get_instructor(instructor_id: int, db: _orm.Session):
    instructor = await _instructor_selector(instructor_id=instructor_id, db=db)

    return _schemas.Instructor.from_orm(instructor)


async def delete_instructor(instructor_id: int, db: _orm.Session):
    instructor = await _instructor_selector(instructor_id=instructor_id, db=db)

    db.delete(instructor)
    db.commit()


async def update_instructor(instructor_id: int, instructor: _schemas.Instructor, db: _orm.Session):
    instructor_obj = await _instructor_selector(instructor_id=instructor_id, db=db)

    instructor_obj.name = instructor.name
    instructor_obj.about = instructor.about
    instructor_obj.profession = instructor.profession

    db.commit()
    db.refresh(instructor_obj)

    return _schemas.Instructor.from_orm(instructor_obj)
