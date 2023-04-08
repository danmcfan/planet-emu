from planet_emu.api.models import Result
from planet_emu.api.schemas import Features
from sqlalchemy.orm import Session


def create_result(
    db: Session, id: str, features: Features, prediction: float
) -> Result:
    result = Result(id=id, features=features, prediction=prediction)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_results(db: Session, skip: int = 0, limit: int = 100) -> list[Result]:
    return db.query(Result).offset(skip).limit(limit).all()


def get_result(db: Session, id: str) -> Result:
    return db.query(Result).filter(Result.id == id).first()
