import json
import time

import ee
import shapely

from src.geojson import write_polygons_to_geojson_file
from src.grid import create_polygons_grid
from src.reduce import reduce_regions

DELTA = 0.05
SCALE_FACTOR = 100_000

SCALE = int(DELTA * SCALE_FACTOR)


def main():
    print("Initializing...")
    credentials = ee.ServiceAccountCredentials(
        "default@ee-danmcfan.iam.gserviceaccount.com", ".private-key.json"
    )
    ee.Initialize(credentials)

    print("Creating feature collection...")
    polygons = create_polygons_grid(delta_x=DELTA, delta_y=DELTA)
    print(f"Count of grid polygons: {len(polygons)}")

    write_polygons_to_geojson_file(polygons, f"data/raw/{SCALE}/grid.geojson")

    features = [
        ee.Feature(
            {
                "type": "Feature",
                "id": str(index),
                "properties": {},
                "geometry": json.loads(shapely.to_geojson(polygon)),
            }
        )
        for index, polygon in enumerate(polygons)
    ]

    for layer, image_name in [
        ("bulkdens", "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02"),
        ("clay", "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02"),
        ("ocarbon", "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02"),
        ("ph", "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02"),
        ("sand", "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02"),
        ("water", "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01"),
    ]:
        print(f"Reducing regions for {layer}...")
        t0 = time.perf_counter()
        image = ee.Image(image_name)
        output_features = reduce_regions(image, features, SCALE)
        print(f"Elapsed time: {time.perf_counter() - t0}")

        print("Writing to file...")
        with open(f"data/raw/{SCALE}/{layer}.geojson", "w") as f:
            json.dump({"type": "FeatureCollection", "features": output_features}, f)

    for layer, image_collection_name in [
        ("daymet", "NASA/ORNL/DAYMET_V4"),
        ("landsat", "LANDSAT/LC09/C02/T1_L2"),
    ]:
        print(f"Reducing regions for {layer}...")
        t0 = time.perf_counter()
        image: ee.Image = (
            ee.ImageCollection(image_collection_name)
            .filterDate("2023-07-01", "2023-07-31")
            .reduce(reducer=ee.Reducer.mean())
        )

        output_features = reduce_regions(image, features, SCALE)
        print(f"Elapsed time: {time.perf_counter() - t0}")

        print("Writing to file...")
        with open(f"data/raw/{SCALE}/{layer}.geojson", "w") as f:
            json.dump({"type": "FeatureCollection", "features": output_features}, f)

    with open(f"data/raw/{SCALE}/grid.geojson", "r") as f:
        features = json.load(f)["features"]

    for filename in [
        "bulkdens",
        "clay",
        "ocarbon",
        "ph",
        "sand",
        "water",
        "daymet",
        "landsat",
    ]:
        with open(f"data/raw/{SCALE}/{filename}.geojson", "r") as f:
            property_features_list = json.load(f)["features"]

        property_features = {
            feature["id"]: feature for feature in property_features_list
        }
        for feature in features:
            property_feature = property_features[feature["id"]]
            for property, value in property_feature["properties"].items():
                feature["properties"][f"{filename}_{property}"] = value

    for feature in features:
        red = feature["properties"]["landsat_SR_B4_mean"]
        nir = feature["properties"]["landsat_SR_B5_mean"]
        feature["properties"]["landsat_ndvi_mean"] = (
            None if red is None or nir is None else ((nir - red) / (nir + red))
        )

    with open(f"data/final/{SCALE}/grid.geojson", "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)


if __name__ == "__main__":
    main()
