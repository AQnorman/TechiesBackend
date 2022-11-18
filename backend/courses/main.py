import fastapi as _fastapi
import fastapi.security as _security
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from dependencies import get_db
from typing import List
from auth.auth_bearer import JWTBearer

router = _fastapi.APIRouter(prefix="/api/courses")


@router.post("/", dependencies=[_fastapi.Depends(JWTBearer())])
async def create_course(course: _schemas.CourseCreate, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.create_course(db=db, course=course)


@router.get("/", response_model=List[_schemas.Course])
async def get_courses(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_courses(db=db)


@router.get("/{course_id}", status_code=200)
async def get_course(course_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_course(course_id=course_id, db=db)


@router.delete("/{course_id}", dependencies=[_fastapi.Depends(JWTBearer())], status_code=204)
async def delete_course(course_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.delete_course(course_id=course_id, db=db)


@router.put("/{course_id}", dependencies=[_fastapi.Depends(JWTBearer())], status_code=200)
async def update_course(course_id: int, course: _schemas.Course, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.update_course(course_id=course_id, course=course, db=db)
    return {"message": "Successfully Updated"}
