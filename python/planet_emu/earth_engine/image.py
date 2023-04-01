import warnings

warnings.simplefilter("ignore", FutureWarning)

import ee
import eeconvert
import geopandas as gpd
from planet_emu.earth_engine.enum import ImageEnum


def create_image(enum: ImageEnum) -> ee.Image:
    return ee.Image(enum.name)


def add_ndvi_band(image: ee.Image) -> ee.Image:
    return image.normalizedDifference(
        ["sur_refl_b02_mean", "sur_refl_b01_mean"]
    ).rename("ndvi")


def reduce_regions(
    image: ee.Image,
    input_gdf: gpd.GeoDataFrame,
    reducer: ee.Reducer = ee.Reducer.mean(),
    scale: int = 30,
    tile_scale: int = 1,
) -> gpd.GeoDataFrame:
    input_crs = input_gdf.crs

    projected_input_gdf = input_gdf.to_crs("EPSG:4326")
    input_fc = eeconvert.gdfToFc(projected_input_gdf)

    output_fc = image.reduceRegions(
        input_fc,
        reducer=reducer,
        scale=scale,
        tileScale=tile_scale,
        crs="EPSG:4326",
    )

    output_gdf = eeconvert.fcToGdf(output_fc)
    projected_output_gdf = output_gdf.to_crs(input_crs)

    return projected_output_gdf
