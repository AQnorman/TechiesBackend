import auth
import courses
import enrollments
import instructors
import feedbacks
from auth import main, models
from courses import main, models
from enrollments import main
from instructors import main, models
from feedbacks import main, models

from database.database import engine

import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware
import tempfile

auth.models.Base.metadata.create_all(bind=engine)
courses.models.Base.metadata.create_all(bind=engine)
feedbacks.models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app = _fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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
app.include_router(instructors.main.router)
app.include_router(feedbacks.main.router)
