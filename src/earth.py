import ee
import eeconvert
import geopandas as gpd

ee.Initialize()


IMAGE_COLLECTION_NAMES = {
    "weather": "NASA/ORNL/DAYMET_V4",
    "crop": "USDA/NASS/CDL",
    "sentinel": "COPERNICUS/S2_SR_HARMONIZED",
}


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
