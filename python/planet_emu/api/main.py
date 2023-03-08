from uuid import uuid4

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware


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
    title="planet-emu-api",
    description="Planet Emulator API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def index():
    return {
        "message": "Go to https://api.planet-emu.com/docs for complete API documentation."
    }


@app.post("/jobs/")
def create_job(point: schemas.Point, db: Session = Depends(get_db)) -> schemas.Job:
    if not (-124.763068 <= point.x <= -66.949895):
        raise HTTPException(400, "X coordinate is out of range")
    if not (24.523096 <= point.y <= 49.384358):
        raise HTTPException(400, "Y coordinate is out of range")

    job_id = uuid4().hex[:8]

    return crud.create_job(db, job_id, point)


@app.get("/jobs/{job_id}")
def get_status(job_id: str, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(400, "Job not found")

    return job


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
