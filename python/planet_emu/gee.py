from typing import Optional
import ee
import eeconvert
import geopandas as gpd
import numpy as np
import requests
import os
import io


def init(
    name: str,
    project: str,
    secret_json: Optional[str] = None,
) -> None:
    if secret_json is None:
        home = os.getenv("HOME")
        secret_json = f"{home}/secrets/service_account.json"

    domain = "iam.gserviceaccount.com"
    service_account = f"{name}@{project}.{domain}"
    credentials = ee.ServiceAccountCredentials(service_account, secret_json)
    ee.Initialize(credentials)


def list_image_info(ic_name: str) -> list[dict]:
    ic = ee.ImageCollection(ic_name).filterDate("2020-01-01", "2021-01-01")
    images = ic.toList(1000)
    for image in images.getInfo():
        print(image["id"])


def get_mean_image_sample(
    img_collection: str,
    in_gdf: gpd.GeoDataFrame,
    year: int,
    scale: float = 10,
) -> gpd.GeoDataFrame:
    in_fc = eeconvert.gdfToFc(in_gdf)

    img = (
        ee.ImageCollection(img_collection)
        .filterDate(f"{year}-01-01", f"{year+1}-01-01")
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

    if len(out_fc.getInfo()["features"]) == 0:
        print("No features returned from spatial query.")
        return gpd.GeoDataFrame()

    return eeconvert.fcToGdf(out_fc)


def get_rgb_numpy_array(
    in_gdf: gpd.GeoDataFrame,
    year: int,
    scale: float = 10,
) -> np.ndarray:
    in_fc = eeconvert.gdfToFc(in_gdf)
    feature = in_fc.first()
    geometry = ee.Geometry(feature.get("geom"))

    img = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(f"{year}-01-01", f"{year+1}-01-01")
        .filterBounds(in_fc)
        .mean()
    )

    url = img.getDownloadUrl(
        {
            "bands": ["B3", "B8", "B11"],
            "region": geometry,
            "scale": scale,
            "format": "NPY",
        }
    )
    response = requests.get(url)
    data = np.load(io.BytesIO(response.content))

    return data


def get_rgb_tif(
    output_tif: str,
    in_gdf: gpd.GeoDataFrame,
    year: int,
    scale: float = 10,
) -> np.ndarray:
    in_fc = eeconvert.gdfToFc(in_gdf)
    feature = in_fc.first()
    geometry = ee.Geometry(feature.get("geom"))

    img = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(f"{year}-01-01", f"{year+1}-01-01")
        .filterBounds(in_fc)
        .mean()
    )

    url = img.getDownloadUrl(
        {
            "bands": ["B3", "B8", "B11"],
            "region": geometry,
            "scale": scale,
            "format": "GEO_TIFF",
        }
    )
    response = requests.get(url)

    with open(output_tif, "wb") as fd:
        fd.write(response.content)
