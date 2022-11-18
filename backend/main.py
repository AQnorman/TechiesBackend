import auth
import courses
import enrollments
from auth import main, models
from courses import main, models
from enrollments import main

from database.database import engine

import fastapi as _fastapi
import tempfile

auth.models.Base.metadata.create_all(bind=engine)
courses.models.Base.metadata.create_all(bind=engine)

app = _fastapi.FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Techies Backend"}


@app.get("/get-tmp")
async def read_tmp():
    return {"message": "{}".format(tempfile.gettempdir())}

# _services.create_database()
app.include_router(auth.main.router)
app.include_router(courses.main.router)
app.include_router(enrollments.main.router)
