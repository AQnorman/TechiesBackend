import fastapi as _fastapi
from courses import schemas as _CourseSchema
from auth import schemas as _UserSchema
import sqlalchemy.orm as _orm
from dependencies import get_db
from . import services as _services
from auth.auth_bearer import JWTBearer

router = _fastapi.APIRouter(prefix="/api/course", tags=["Enroll"])


@router.put("/enroll", dependencies=[_fastapi.Depends(JWTBearer())], status_code=200)
async def add_user_to_course(course_id: int, user_id: int, db: _orm.Session = _fastapi.Depends(get_db)):
    await _services.add_user_to_course(db=db, user_id=user_id, course_id=course_id)
