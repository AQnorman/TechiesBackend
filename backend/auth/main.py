import fastapi as _fastapi
import fastapi.security as _security
from . import schemas as _schemas
from . import services as _services
import sqlalchemy.orm as _orm
from courses import schemas as _CourseSchema
from typing import Union
from . import auth_bearer as _auth_bearer

router = _fastapi.APIRouter(prefix="/api")


@router.post("/users")
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="The Email is already in use.")

    user = await _services.create_user(db=db, user=user)

    return await _auth_bearer.signJWT(user)


@router.post("/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")

    return await _auth_bearer.signJWT(user)


@router.post("/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user
