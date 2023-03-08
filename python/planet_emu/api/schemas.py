from enum import Enum
from typing import Any

from pydantic import BaseModel


class Point(BaseModel):
    x: float
    y: float


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"


class Job(BaseModel):
    id: str
    x: float
    y: float
    status: Status = Status.PENDING
    result: dict[str, float] | None = None

    class Config:
        orm_mode = True


class Task(BaseModel):
    id: str
    status: str
    result: Any

    class Config:
        orm_mode = True
