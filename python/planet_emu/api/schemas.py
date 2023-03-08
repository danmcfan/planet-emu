from typing import Any, Hashable

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    status: str
    result: Any

    class Config:
        orm_mode = True


class Result(BaseModel):
    id: str
    x: float
    y: float
    year: int
    properties: dict[Hashable, Any]

    class Config:
        orm_mode = True
