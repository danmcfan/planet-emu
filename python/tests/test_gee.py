import logging
import os
import random

from dotenv import load_dotenv
import ee
import geopandas as gpd
from shapely import geometry

from planet_emu.gee import (
    get_mean_image_sample,
    get_rgb_numpy_array,
    get_rgb_tif,
    init,
    list_image_info,
)


logger = logging.getLogger(__name__)

load_dotenv()

NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")

polygons = []
for _ in range(10):
    x = random.uniform(-100, -80)
    y = random.uniform(30, 50)

    centroid = geometry.Point(x, y)
    polygon = centroid.buffer(0.001)

    polygons.append(polygon)

input_gdf = gpd.GeoDataFrame(geometry=polygons, crs="EPSG:4326")


def test_vars() -> None:
    assert NAME is not None
    assert PROJECT is not None


def test_init() -> None:
    init(NAME, PROJECT, "service_account.json")


def test_get_image_collection_info():
    image_collection_info = (
        ee.ImageCollection("NASA/ORNL/DAYMET_V4")
        .filterDate("2020-01-01", "2020-02-01")
        .getInfo()
    )

    for key in ("type", "bands", "id", "version", "properties", "features"):
        assert key in image_collection_info


def test_list_image_info():
    image_info = list_image_info("NASA/ORNL/DAYMET_V4")
    assert len(image_info) > 0

    for item in image_info:
        for key in ("type", "bands", "version", "id", "properties"):
            assert key in item


def test_get_mean_image_sample():
    output_gdf = get_mean_image_sample("NASA/ORNL/DAYMET_V4", input_gdf, 2020)

    assert isinstance(output_gdf, gpd.GeoDataFrame)
    assert len(output_gdf) > 0

    output_gdf.to_csv(".temp/output.csv")
