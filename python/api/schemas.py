from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"


class Features(BaseModel):
    bulk_density_b0: Decimal
    bulk_density_b10: Decimal
    bulk_density_b100: Decimal
    bulk_density_b200: Decimal
    bulk_density_b30: Decimal
    bulk_density_b60: Decimal
    clay_b0: Decimal
    clay_b10: Decimal
    clay_b100: Decimal
    clay_b200: Decimal
    clay_b30: Decimal
    clay_b60: Decimal
    organic_carbon_b0: Decimal
    organic_carbon_b10: Decimal
    organic_carbon_b100: Decimal
    organic_carbon_b200: Decimal
    organic_carbon_b30: Decimal
    organic_carbon_b60: Decimal
    ph_b0: Decimal
    ph_b10: Decimal
    ph_b100: Decimal
    ph_b200: Decimal
    ph_b30: Decimal
    ph_b60: Decimal
    sand_b0: Decimal
    sand_b10: Decimal
    sand_b100: Decimal
    sand_b200: Decimal
    sand_b30: Decimal
    sand_b60: Decimal
    water_content_b0: Decimal
    water_content_b10: Decimal
    water_content_b100: Decimal
    water_content_b200: Decimal
    water_content_b30: Decimal
    water_content_b60: Decimal
    prcp: Decimal
    srad: Decimal
    swe: Decimal
    tmax: Decimal
    tmin: Decimal
    vp: Decimal


class Task(BaseModel):
    id: str
    status: Status
    features: Features
    prediction: Decimal | None = None
