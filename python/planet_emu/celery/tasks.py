import json
from typing import Protocol, Hashable, Any

from planet_emu.api.database import SessionLocal
from planet_emu.api import crud, schemas
from planet_emu.celery import celery
from planet_emu.predict import predict_features


class Request(Protocol):
    id: str


class Task(Protocol):
    request: Request


@celery.task(bind=True)
def predict_features_task(self: Task, features: dict[Hashable, Any]):
    features = schemas.Features(**features)
    prediction = predict_features(features)

    db = SessionLocal()

    try:
        crud.create_result(db, self.request.id, features.dict(), prediction)
    finally:
        db.close()
