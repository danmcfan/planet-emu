from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from planet_emu.api import crud, models, schemas
from planet_emu.api.database import SessionLocal, engine

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


@app.post("/jobs/", response_model=schemas.Job)
def create_job(point: schemas.Point, db: Session = Depends(get_db)):
    if not (-124.763068 <= point.x <= -66.949895):
        raise HTTPException(400, "X coordinate is out of range")
    if not (24.523096 <= point.y <= 49.384358):
        raise HTTPException(400, "Y coordinate is out of range")

    job_id = uuid4().hex[:8]

    return crud.create_job(db, job_id, point)


@app.get("/jobs/", response_model=list[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_jobs(db, skip=skip, limit=limit)


@app.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: str, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(400, "Job not found")

    return job
