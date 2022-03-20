import ee
import eeconvert
import geopandas as gpd
import pandas as pd
import datetime as dt
import time

ee.Initialize()


IMAGE_COLLECTION_NAMES = {
    "weather": "NASA/ORNL/DAYMET_V4",
    "reflectance": "MODIS/006/MOD09Q1",
    "crop": "USDA/NASS/CDL",
}


def get_mean_image_sample(
    img_collection: str,
    in_gdf: gpd.GeoDataFrame,
    scale: int,
    month: int,
    year: int = 2020,
) -> pd.DataFrame:
    in_fc = eeconvert.gdfToFc(in_gdf)

    next_month = month + 1

    if next_month > 12:
        next_month = 1
        next_year = year + 1
    else:
        next_year = year

    img = (
        ee.ImageCollection(img_collection)
        .filterDate(f"{year}-{month}-01", f"{next_year}-{next_month}-01")
        .filterBounds(in_fc)
        .mean()
    )

    out_fc = img.sampleRegions(
        in_fc,
        properties=[],
        projection=ee.Projection("EPSG:4326"),
        scale=scale,
        geometries=True,
    )

    out_gdf = eeconvert.fcToGdf(out_fc)

    return out_gdf, img


def export_to_drive(
    image: ee.Image,
    file_name: str,
    in_gdf: gpd.GeoDataFrame,
    scale: int,
    delay: int = 10,
) -> None:

    task = ee.batch.Export.image.toDrive(
        image=image,
        description=file_name,
        folder="exports",
        scale=scale,
        region=eeconvert.gdfToFc(in_gdf),
    )

    task.start()

    while task.active():
        print("Task is active...")
        time.sleep(delay)

    return task
