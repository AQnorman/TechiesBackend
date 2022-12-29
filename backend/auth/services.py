import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import passlib.hash as _hash
import sqlalchemy.orm as _orm
from dependencies import get_db
import json
from database import database as _database
from . import models as _models
from . import schemas as _schemas

from utils import oauth2schema, JWT_SECRET
from . import auth_bearer

# USERS


# GET USER BY ID
async def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id and _models.User.role == "student").first()


# GET ADMIN BY ID
async def get_admin(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id and _models.User.role == "admin").first()


# GET USER BY EMAIL
async def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email and _models.User.role == "student").first()


# GET ADMIN BY EMAIL
async def get_admin_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email and _models.User.role == "admin").first()


# GET ALL USERS
async def get_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).filter(_models.User.role == "student").offset(skip).limit(limit).all()


# GET ALL ADMINS
async def get_admins(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).filter(_models.User.role == "admin").offset(skip).limit(limit).all()


# CREATE USER
async def create_user(db: _orm.Session, user: _schemas.UserCreate):
    user_obj = _models.User(username=user.username,
                            email=user.email,
                            phone=user.phone,
                            hashed_password=_hash.bcrypt.hash(
                                user.hashed_password),
                            role="student")
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


# CREATE ADMIN
async def create_admin(db: _orm.Session, user: _schemas.AdminCreate):
    user_obj = _models.User(
        email=user.email,
        hashed_password=_hash.bcrypt.hash(
            user.hashed_password
        ),
        role="admin"
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


# AUTHENTICATE USER
async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


# CREATE TOKEN
async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: _orm.Session = _fastapi.Depends(get_db), token: str = _fastapi.Depends(oauth2schema)):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
        print(user)
    except:
        raise _fastapi.HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)


async def get_current_admin(db: _orm.Session = _fastapi.Depends(get_db), token: str = _fastapi.Depends(oauth2schema)):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
        print(user)
    except:
        raise _fastapi.HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return _schemas.Admin.from_orm(user)


async def update_user(user_id: int, user: _schemas.UserCreate, db: _orm.Session):
    user_obj = db.query(_models.User).filter(
        _models.User.id == user_id).first()

    if user_obj is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="User Not Found."
        )

    if user.email == user_obj.email:
        user_obj.username = user.username
        user_obj.phone = user.phone
    else:
        user_obj.username = user.username
        user_obj.email = user.email
        user_obj.phone = user.phone

    if user.hashed_password == "":
        user_obj.hashed_password = user_obj.hashed_password
    else:
        user_obj.hashed_password = _hash.bcrypt.hash(user.hashed_password)

    db.commit()
    db.refresh(user_obj)

    return {"message": "success", "username": user_obj.username, "email": user_obj.email, "phone": user_obj.phone}
