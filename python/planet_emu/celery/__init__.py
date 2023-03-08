import os

from celery import Celery

broker = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

celery = Celery(
    __name__,
    backend=backend,
    broker=broker,
    include=["planet_emu.celery.tasks"],
)

print(__name__)
