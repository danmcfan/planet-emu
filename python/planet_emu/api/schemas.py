from enum import Enum, auto

from pydantic import BaseModel


class Point(BaseModel):
    x: float
    y: float


class Status(str, Enum):
    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILURE = auto()


class Job(BaseModel):
    id: str
    x: float
    y: float
    status: Status = Status.PENDING
    result: dict[str, float] | None = None

    class Config:
        orm_mode = True
