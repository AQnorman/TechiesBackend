import fastapi as _fastapi
import fastapi.security as _security
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from courses import schemas as _CourseSchema
from typing import Union
from . import auth_bearer as _auth_bearer

router = _fastapi.APIRouter(prefix="/api")


@router.post("/users", tags=["User"])
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="The Email is already in use.")

    user = await _services.create_user(db=db, user=user)

    return await _auth_bearer.signJWT(user)


@router.post("/admins", tags=["Admin"])
async def create_admin(user: _schemas.AdminCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_admin = await _services.get_admin_by_email(db=db, email=user.email)

    if db_admin:
        raise _fastapi.HTTPException(
            status_code=400, detail="The Email is already in use."
        )

    admin = await _services.create_admin(db=db, user=user)

    return await _auth_bearer.signAdminJWT(admin)


@router.get("/users", tags=["User"], response_model=list[_schemas.User])
async def get_users(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_users(db=db)


@router.get("/admins", tags=["Admin"], response_model=list[_schemas.Admin])
async def get_admins(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_admins(db=db)


@router.post("/token", tags=["User"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")

    if user.role == "student":
        return await _auth_bearer.signJWT(user)
    elif user.role == "admin":
        return await _auth_bearer.signAdminJWT(user)


@router.post("/users/me", response_model=_schemas.User, tags=["User"])
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@router.post("/admins/me", response_model=_schemas.Admin, tags=["Admin"])
async def get_user(user: _schemas.Admin = _fastapi.Depends(_services.get_current_admin)):
    return user


@router.put("/users/{user_id}", tags=["User"])
async def update_user(user_id: int, user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    res = await _services.update_user(user_id=user_id, user=user, db=db)
    return res


@router.put("/admins/{user_id}", tags=["Admin"])
async def update_admin(user_id: int, user: _schemas.AdminCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    res = await _services.update_admin(user_id=user_id, user=user, db=db)
    return res
