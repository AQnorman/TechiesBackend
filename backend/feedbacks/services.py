import fastapi as _fastapi
import datetime as _dt
from auth import schemas as _UserSchema
from auth import models as _UserModel
from . import schemas as _FeedbackSchema
from . import models as _FeedbackModel
import sqlalchemy.orm as _orm


async def create_feedback(feedback: _FeedbackSchema.FeedbackCreate, student_id: int, db: _orm.Session):
    student = db.query(_UserModel.User).filter(
        _UserModel.User.id == student_id).first()

    if student is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="Student Not Found."
        )

    feedback = _FeedbackModel.Feedback(
        **feedback.dict(), student_id=student_id)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


async def get_feedbacks(db: _orm.Session):
    feedbacks = db.query(_FeedbackModel.Feedback)
    return list(map(_FeedbackSchema.Feedback.from_orm, feedbacks))


async def _feedback_selector(feedback_id: int, db: _orm.Session):
    feedback = (
        db.query(_FeedbackModel.Feedback).filter(
            _FeedbackModel.Feedback.id == feedback_id).first()
    )

    if feedback is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Feedback Not Found."
        )

    return feedback


async def get_feedback(feedback_id: int, db: _orm.Session):
    feedback = await _feedback_selector(feedback_id=feedback_id, db=db)

    return _FeedbackSchema.Feedback.from_orm(feedback)


async def delete_feedback(feedback_id: int, db: _orm.Session):
    feedback = await _feedback_selector(feedback_id=feedback_id, db=db)

    db.delete(feedback)
    db.commit()


async def update_feedback(feedback_id: int, feedback: _FeedbackSchema.Feedback, db: _orm.Session):
    feedback_obj = await _feedback_selector(feedback_id=feedback_id, db=db)

    feedback_obj.feedback = feedback.feedback
    feedback_obj.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(feedback_obj)

    return _FeedbackSchema.Feedback.from_orm(feedback_obj)
