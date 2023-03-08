import warnings
from typing import Any

warnings.simplefilter("ignore", FutureWarning)

import os

import geopandas as gpd
import pandas as pd
from shapely import geometry

from planet_emu import gee

NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")

gee.init(NAME, PROJECT, "service_account.json")

from planet_emu import image, predict
from planet_emu.api import util


def handler(event: dict, context: Any) -> dict:
    year = event.get("year", 2020)

    x, y, job_id = event["x"], event["y"], event["job_id"]
    point = geometry.Point(x, y)
    circle = point.buffer(0.01, resolution=4)

    gdf = gpd.GeoDataFrame(geometry=[circle], crs="EPSG:4326")

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

    data = pd.DataFrame(data, index=[0])

    features = data.drop(columns=["ndvi"])

    dirpath = os.path.dirname(os.path.realpath(__file__))

    linear_model = predict.load_model(f"{dirpath}/model/linear")
    data["linear_ndvi"] = linear_model.predict(features).flatten()

    dnn_model = predict.load_model(f"{dirpath}/model/dnn")
    data["dnn_ndvi"] = dnn_model.predict(features).flatten()

    data["x"] = x
    data["y"] = y
    data["status"] = "done"

    util.set_json(data.to_dict(orient="records"), job_id)

    return {
        "job_id": job_id,
        "data": data.to_dict(orient="records")[0],
    }
