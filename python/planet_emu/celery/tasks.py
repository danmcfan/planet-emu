import warnings
from typing import Protocol

warnings.simplefilter("ignore", FutureWarning)

import os

import geopandas as gpd
import pandas as pd
from shapely import geometry

from planet_emu.api.crud import create_result
from planet_emu.api.database import SessionLocal
from planet_emu.celery import celery
from planet_emu.gee import init

NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")

if NAME is None:
    raise ValueError("GCP_SERVICE_NAME is not set")
if PROJECT is None:
    raise ValueError("GCP_PROJECT is not set")

init(NAME, PROJECT)

from planet_emu import image


class Request(Protocol):
    id: str


class Task(Protocol):
    request: Request


@celery.task(bind=True)
def predict_point(self: Task, x: float, y: float, year: int = 2020):
    point = geometry.Point(x, y)
    circle = point.buffer(0.01, resolution=4)

    gdf = gpd.GeoDataFrame(geometry=[circle], crs="EPSG:4326")  # type: ignore

    data = {}
    for image_object, name in [
        (image.BULKDENS_IMG, "bulkdens"),
        (image.CLAY_IMG, "clay"),
        (image.PH_IMG, "ph"),
        (image.SAND_IMG, "sand"),
        (image.SOC_IMG, "soc"),
        (image.SWC_IMG, "swc"),
    ]:
        result_gdf = (
            image_object.reduce_regions(gdf)
            .rename(columns=lambda x: x.replace("b", f"{name}_"))
            .drop(columns=["geometry"])
        )
        data.update(result_gdf.to_dict(orient="records")[0])

    for image_collection_object, name in [
        (image.WEATHER_IC, "weather"),
        (image.MODIS_IC, "modis"),
    ]:
        image_object = image_collection_object.get_reduced_image(
            "mean", f"{year}-01-01", f"{year+1}-01-01"
        )

        if name == "modis":
            image_object.set_ndvi()

        result_gdf = (
            image_object.reduce_regions(gdf)
            .rename(columns={"mean": "ndvi"})
            .drop(columns=["geometry"])
        )
        data.update(result_gdf.to_dict(orient="records")[0])

    df = pd.DataFrame(data, index=[0])

    data = df.to_dict(orient="records")[0]

    db = SessionLocal()

    try:
        create_result(db=db, id=self.request.id, x=x, y=y, year=year, properties=data)
    finally:
        db.close()
