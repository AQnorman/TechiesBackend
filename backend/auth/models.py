import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import enum
from database.database import Base


class User(Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, index=True, default=None)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    phone = _sql.Column(_sql.Integer, index=True, default=None)
    is_active = _sql.Column(_sql.Boolean, default=True)
    role = _sql.Column(_sql.String, index=True)

    courses = _orm.relationship("Course", back_populates="student")
    feedbacks = _orm.relationship("Feedback", back_populates="student")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
