import warnings
from typing import Protocol

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
from shapely import geometry

from planet_emu.api.crud import create_result
from planet_emu.api.database import SessionLocal
from planet_emu.celery import celery
from planet_emu.earth_engine import image, collection, enum


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

    for member in enum.ImageEnum:
        image_object = image.create_image(member)
        result = (
            image.reduce_regions(image_object, gdf, scale=member.scale, tile_scale=1)
            .rename(columns=lambda col: col.replace("b", f"{member.value}_"))
            .drop(columns=["geometry"])
        )

        result_dict = result.to_dict(orient="records")[0]
        data.update(result_dict)

    member = enum.ImageCollectionEnum.WEATHER
    image_collection = collection.create_image_collection(member)
    image_collection = collection.filter_by_date(
        image_collection, f"{year}-01-01", f"{year+1}-01-01"
    )

    image_object = collection.reduce_collection(image_collection)
    result = image.reduce_regions(
        image_object, gdf, scale=member.scale, tile_scale=1
    ).drop(columns=["geometry"])

    result_dict = result.to_dict(orient="records")[0]
    data.update(result_dict)

    member = enum.ImageCollectionEnum.SPECTRAL
    image_collection = collection.create_image_collection(member)
    image_collection = collection.filter_by_date(
        image_collection, f"{year}-01-01", f"{year+1}-01-01"
    )

    image_object = collection.reduce_collection(image_collection)
    image_object = image.add_ndvi_band(image_object)
    result = (
        image.reduce_regions(image_object, gdf, scale=member.scale, tile_scale=1)
        .rename(columns={"mean": "ndvi"})
        .drop(columns=["geometry"])
    )

    result_dict = result.to_dict(orient="records")[0]
    data.update(result_dict)

    db = SessionLocal()

    try:
        create_result(db=db, id=self.request.id, x=x, y=y, year=year, properties=data)
    finally:
        db.close()
