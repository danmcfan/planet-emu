import os
import time

from celery import Celery

broker = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery = Celery(__name__, broker=broker, backend=backend)


@celery.task
def create_task(task_type) -> bool:
    time.sleep(int(task_type) * 10)
    return True
