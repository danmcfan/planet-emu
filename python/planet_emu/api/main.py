from uuid import uuid4

from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from planet_emu.api import crud, models, schemas
from planet_emu.api.database import SessionLocal, engine
from planet_emu.celery import celery
from planet_emu.celery.tasks import predict_point

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="Planet Emu",
    description="An emulator of the planet Earth",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/", response_class=RedirectResponse, status_code=302)
def index():
    return "https://api.planet-emu.com/docs"


@app.post("/tasks/", response_model=schemas.Task)
def create_task(x: float, y: float, year: int = 2020):
    if not (-124.763068 <= x <= -66.949895):
        raise HTTPException(400, "X coordinate is out of range")
    if not (24.523096 <= y <= 49.384358):
        raise HTTPException(400, "Y coordinate is out of range")
    if not (2000 <= year <= 2020):
        raise HTTPException(400, "Year is out of range")

    return predict_point.delay(x, y, year)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: str):
    return AsyncResult(task_id, app=celery)


@app.get("/results", response_model=list[schemas.Result])
def read_results(db: Session = Depends(get_db)):
    return crud.get_results(db)


@app.get("/result/{task_id}", response_model=schemas.Result)
def read_result(task_id: str, db: Session = Depends(get_db)):
    result = crud.get_result(db, task_id)

    if result is None:
        raise HTTPException(404, "Result not found")

    return result
