import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

from database.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    feedback = _sql.Column(_sql.String, index=True)
    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    student = _orm.relationship("User", back_populates="feedbacks")
