import fastapi as _fastapi
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from dependencies import get_db
from auth.auth_bearer import JWTBearer
from typing import List


router = _fastapi.APIRouter(prefix="/api/instructors", tags=["Instructors"])


@router.post("/")
async def create_instructor(instructor: _schemas.InstructorCreate, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.create_instructor(db=db, instructor=instructor)


@router.get("/", response_model=List[_schemas.Instructor])
async def get_instructors(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_instructors(db=db)


@router.get("/{instructor_id}", status_code=200)
async def get_instructor(instructor_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_instructor(instructor_id=instructor_id, db=db)


@router.delete("/{instructor_id}", status_code=204)
async def delete_instructor(instructor_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.delete_instructor(instructor_id=instructor_id, db=db)


@router.put("/{instructor_id}", status_code=200)
async def update_instructor(instructor_id: int, instructor: _schemas.Instructor, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.update_instructor(
        instructor=instructor, instructor_id=instructor_id, db=db
    )

    return {"message": "Instructor Successfully Updated"}
