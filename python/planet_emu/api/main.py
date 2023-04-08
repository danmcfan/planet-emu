from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from planet_emu.api import crud, models, schemas
from planet_emu.api.database import SessionLocal, engine
from planet_emu.celery import celery
from planet_emu.celery.tasks import predict_features_task
from sqlalchemy.orm import Session

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
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
        "https://planet-emu.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/", response_class=RedirectResponse, status_code=302)
def index():
    return "https://api.planet-emu.com/docs"


@app.post("/tasks", response_model=schemas.Task, status_code=201)
def create_task(features: schemas.Features):
    task: AsyncResult = predict_features_task.delay(features=features.dict())
    return schemas.Task(id=task.id, status=task.status)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: str):
    task = AsyncResult(task_id, app=celery)
    return schemas.Task(id=task.id, status=task.status)


@app.get("/results", response_model=list[schemas.Result])
def read_results(db: Session = Depends(get_db)):
    return crud.get_results(db)


@app.get("/results/{task_id}", response_model=schemas.Result)
def read_result(task_id: str, db: Session = Depends(get_db)):
    result = crud.get_result(db, task_id)

    if result is None:
        raise HTTPException(404, "Result not found")

    return result


@app.delete("/results/{task_id}", status_code=204)
def delete_result(task_id: str, db: Session = Depends(get_db)):
    result = crud.get_result(db, task_id)

    if result is None:
        raise HTTPException(404, "Result not found")

    db.delete(result)
    db.commit()
