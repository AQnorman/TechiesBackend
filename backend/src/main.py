from . import auth, courses, enrollments
from .auth import main, models
from .courses import main, models
from .enrollments import main

from src.database.database import engine

import fastapi as _fastapi

auth.models.Base.metadata.create_all(bind=engine)
courses.models.Base.metadata.create_all(bind=engine)

app = _fastapi.FastAPI()

# _services.create_database()
app.include_router(auth.main.router)
app.include_router(courses.main.router)
app.include_router(enrollments.main.router)
