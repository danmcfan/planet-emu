import datetime as dt

import ee
from planet_emu.earth_engine.enum import ImageCollectionEnum


def add_ndvi_band(
    image: ee.Image, ndvi_band: str = "sur_refl_b02", red_band: str = "sur_refl_b01"
) -> ee.Image:
    return image.normalizedDifference([ndvi_band, red_band]).rename("ndvi")


def create_image_collection(enum: ImageCollectionEnum) -> ee.ImageCollection:
    return ee.ImageCollection(enum.name)


def filter_by_date(
    collection: ee.ImageCollection,
    start_date: str | dt.datetime,
    end_date: str | dt.datetime,
) -> ee.ImageCollection:
    if isinstance(start_date, dt.datetime):
        start_date = start_date.strftime("%Y-%m-%d")
    if isinstance(end_date, dt.datetime):
        end_date = end_date.strftime("%Y-%m-%d")

    return collection.filterDate(start_date, end_date)


def reduce_collection(
    collection: ee.ImageCollection, reducer: ee.Reducer = ee.Reducer.mean()
) -> ee.Image:
    return collection.reduce(reducer)
