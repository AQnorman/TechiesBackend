import fastapi as _fastapi
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from dependencies import get_db
from typing import List
from auth.auth_bearer import JWTBearer

router = _fastapi.APIRouter(prefix="/api/feedbacks", tags=["Feedbacks"])

# dependencies=[_fastapi.Depends(JWTBearer())]


@router.post("/", response_model=_schemas.Feedback)
async def create_feedback(feedback: _schemas.FeedbackCreate, student_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.create_feedback(db=db, feedback=feedback, student_id=student_id)


@router.get("/", response_model=List[_schemas.Feedback])
async def get_feedbacks(db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_feedbacks(db=db)


@router.get("/{feedback_id}", status_code=200)
async def get_feedback(feedback_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.get_feedback(feedback_id=feedback_id, db=db)


@router.delete("/{feedback_id}", status_code=204)
async def delete_feedback(feedback_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _services.delete_feedback(feedback_id=feedback_id, db=db)


@router.put("/{feedback_id}", status_code=200)
async def update_feedback(feedback_id: int, feedback: _schemas.Feedback, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.update_feedback(feedback_id=feedback_id, feedback=feedback, db=db)

    return {"message": "Successfully Updated"}
