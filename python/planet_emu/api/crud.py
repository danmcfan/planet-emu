from typing import Any, Hashable

from sqlalchemy.orm import Session

from planet_emu.api import models


def create_result(
    db: Session, id: str, x: float, y: float, year: int, properties: dict[Hashable, Any]
) -> models.Result:
    result = models.Result(id=id, x=x, y=y, year=year, properties=properties)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_results(db: Session, skip: int = 0, limit: int = 100) -> list[models.Result]:
    return db.query(models.Result).offset(skip).limit(limit).all()


def get_result(db: Session, id: str) -> models.Result:
    return db.query(models.Result).filter(models.Result.id == id).first()
