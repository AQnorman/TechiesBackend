import sqlalchemy as _sql
import sqlalchemy.orm as _orm

from database.database import Base


class Instructor(Base):
    __tablename__ = "instructors"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    about = _sql.Column(_sql.String, index=True)
    profession = _sql.Column(_sql.String, index=True)

    course = _orm.relationship("Course", back_populates="instructor")
