import ee
import eeconvert
import geopandas as gpd
import time

ee.Initialize()


IMAGE_COLLECTION_NAMES = {
    "weather": "NASA/ORNL/DAYMET_V4",
    "crop": "USDA/NASS/CDL",
    "sentinel": "COPERNICUS/S2_SR_HARMONIZED",
}


def get_mean_image_sample(
    img_collection: str,
    in_gdf: gpd.GeoDataFrame,
    scale: float,
    year: int,
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

    try:
        out_gdf = eeconvert.fcToGdf(out_fc)
    except:
        if len(out_fc.getInfo()["features"]) == 0:
            print("No features returned from spatial query.")
        out_gdf = gpd.GeoDataFrame()

    return out_gdf


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
