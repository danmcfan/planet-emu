from typing import Any

import numpy as np
from pydantic import BaseModel


class Task(BaseModel):
    id: str
    status: str


class Features(BaseModel):
    bulk_density_b0: float
    bulk_density_b10: float
    bulk_density_b100: float
    bulk_density_b200: float
    bulk_density_b30: float
    bulk_density_b60: float
    clay_b0: float
    clay_b10: float
    clay_b100: float
    clay_b200: float
    clay_b30: float
    clay_b60: float
    organic_carbon_b0: float
    organic_carbon_b10: float
    organic_carbon_b100: float
    organic_carbon_b200: float
    organic_carbon_b30: float
    organic_carbon_b60: float
    ph_b0: float
    ph_b10: float
    ph_b100: float
    ph_b200: float
    ph_b30: float
    ph_b60: float
    sand_b0: float
    sand_b10: float
    sand_b100: float
    sand_b200: float
    sand_b30: float
    sand_b60: float
    water_content_b0: float
    water_content_b10: float
    water_content_b100: float
    water_content_b200: float
    water_content_b30: float
    water_content_b60: float
    prcp: float
    srad: float
    swe: float
    tmax: float
    tmin: float
    vp: float

    def to_ndarray(self):
        return np.array([v for _, v in self.dict().items()])


class Result(BaseModel):
    id: str
    features: Features
    prediction: float

    class Config:
        orm_mode = True
