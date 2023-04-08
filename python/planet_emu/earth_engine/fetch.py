import geopandas as gpd
from planet_emu.earth_engine import collection, enum, image
from planet_emu.earth_engine.sample import sample_regions


def fetch_soil(
    grid_gdf: gpd.GeoDataFrame, image_enum: enum.ImageEnum, scale: int
) -> gpd.GeoDataFrame:
    image_obj = image.create_image(image_enum)

    gdf = sample_regions(image_obj, grid_gdf, scale)

    gdf.columns = [f"{image_enum.value}_{col}" for col in gdf.columns[:-1]] + [
        "geometry"
    ]

    return gdf


def fetch_weather(grid_gdf: gpd.GeoDataFrame, scale: int) -> gpd.GeoDataFrame:
    image_collection = collection.create_image_collection(
        enum.ImageCollectionEnum.WEATHER
    )
    image_collection = collection.filter_by_date(
        image_collection, "2000-01-01", "2017-12-31"
    )
    image_obj = collection.reduce_collection(image_collection)

    weather_gdf = sample_regions(image_obj, grid_gdf, scale)

    weather_gdf.columns = [
        "dayl",
        "prcp",
        "srad",
        "swe",
        "tmax",
        "tmin",
        "vp",
        "geometry",
    ]

    weather_gdf = weather_gdf.drop(columns=["dayl"])

    return weather_gdf


def fetch_ndvi(grid_gdf: gpd.GeoDataFrame, scale: int) -> gpd.GeoDataFrame:
    image_collection = collection.create_image_collection(
        enum.ImageCollectionEnum.SPECTRAL
    )
    image_collection = collection.filter_by_date(
        image_collection, "2000-01-01", "2017-12-31"
    )
    image_obj = collection.reduce_collection(image_collection)
    image_obj = collection.add_ndvi_band(
        image_obj, "sur_refl_b02_mean", "sur_refl_b01_mean"
    )

    ndvi_gdf = sample_regions(image_obj, grid_gdf, scale=scale)

    ndvi_gdf.columns = ["ndvi", "geometry"]

    ndvi_gdf["ndvi"] = ndvi_gdf["ndvi"].apply(lambda x: x if x > 0.0 else 0.0)

    return ndvi_gdf
