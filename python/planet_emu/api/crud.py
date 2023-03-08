from sqlalchemy.orm import Session

from planet_emu.api import models, schemas


def create_job(db: Session, id: str, point: schemas.Point) -> models.Job:
    db_job = models.Job(id=id, x=point.x, y=point.y)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[models.Job]:
    return db.query(models.Job).offset(skip).limit(limit).all()


def get_job(db: Session, id: str) -> models.Job:
    return db.query(models.Job).filter(models.Job.id == id).first()
