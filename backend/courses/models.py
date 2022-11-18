import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

from database.database import Base


class Course(Base):
    __tablename__ = "courses"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    desc = _sql.Column(_sql.String, index=True)
    outline = _sql.Column(_sql.String, index=True)
    outcomes = _sql.Column(_sql.String, index=True)
    duration = _sql.Column(_sql.Integer, index=True)
    start_date = _sql.Column(_sql.Date, default=_dt.datetime.date)
    fees = _sql.Column(_sql.Integer, index=True)
    student_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    student = _orm.relationship("User", back_populates="courses")
