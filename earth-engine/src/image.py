from enum import StrEnum
import datetime as dt

import ee
import geemap
import geopandas as gpd


class ImageAsset(StrEnum):
    BULK_DENSITY = "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02"
    CLAY = "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02"
    ORGANIC_CARBON = "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02"
    PH = "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02"
    SAND = "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02"
    WATER_CONTENT = "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01"


class ImageCollectionAsset(StrEnum):
    WEATHER = "NASA/ORNL/DAYMET_V4"
    SPECTRAL = "MODIS/061/MOD09GQ"


def create_image(image_asset: ImageAsset) -> ee.Image:
    return ee.Image(image_asset)


def create_image_collection(
    image_collection_asset: ImageCollectionAsset,
) -> ee.ImageCollection:
    return ee.ImageCollection(image_collection_asset)


def reduce_regions(
    image: ee.Image,
    gdf: gpd.GeoDataFrame,
    reducer: ee.Reducer = ee.Reducer.mean(),
    scale: int | None = None,
    crs: ee.projection.Projection | None = None,
    tileScale: int = 1,
) -> gpd.GeoDataFrame:
    regions = geemap.gdf_to_ee(gdf)

    output_regions = image.reduceRegions(
        regions,
        reducer=reducer,
        scale=scale,
        crs=crs,
        tileScale=tileScale,
    )

    return geemap.ee_to_gdf(output_regions)


def sample_regions(
    image: ee.Image,
    gdf: gpd.GeoDataFrame,
    scale: int | None = None,
    projection: ee.projection.Projection | None = None,
    tileScale: float = 1.0,
) -> gpd.GeoDataFrame:
    regions = geemap.gdf_to_ee(gdf)

    output_regions = image.sampleRegions(
        regions,
        scale=scale,
        projection=projection,
        tileScale=tileScale,
        geometries=True,
    )

    return geemap.ee_to_gdf(output_regions)


def add_ndvi_band_to_image(image: ee.Image) -> ee.Image:
    return image.normalizedDifference(
        ["sur_refl_b02_mean", "sur_refl_b01_mean"]
    ).rename("ndvi")


def filter_image_collection_by_date(
    collection: ee.ImageCollection,
    start_date: str | dt.datetime,
    end_date: str | dt.datetime,
) -> ee.ImageCollection:
    if isinstance(start_date, dt.datetime):
        start_date = start_date.strftime("%Y-%m-%d")
    if isinstance(end_date, dt.datetime):
        end_date = end_date.strftime("%Y-%m-%d")

    return collection.filterDate(start_date, end_date)
