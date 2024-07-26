import json
import time

import ee

from src.grid import create_features_grid
from src.reduce import reduce_regions

MIN_X = -109.05
MAX_X = -102.05

MIN_Y = 36.99
MAX_Y = 41.00

# 0.00001 degrees = 1 meter
DELTA_X = 0.01  # 1 kilometer
DELTA_Y = 0.01  # 1 kilometer


def main():
    print("Initializing...")
    credentials = ee.ServiceAccountCredentials(
        "default@ee-danmcfan.iam.gserviceaccount.com", ".private-key.json"
    )
    ee.Initialize(credentials)

    print("Creating feature collection...")
    features = create_features_grid(MIN_X, MIN_Y, MAX_X, MAX_Y, DELTA_X, DELTA_Y)
    print(f"Count of grid features: {len(features)}")

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
        output_features = reduce_regions(image, features, 250)
        print(f"Elapsed time: {time.perf_counter() - t0}")

        print("Writing to file...")
        with open(f"data/{layer}.geojson", "w") as f:
            json.dump({"type": "FeatureCollection", "features": output_features}, f)

    for layer, image_collection_name in [
        ("daymet", "NASA/ORNL/DAYMET_V4"),
        ("modis", "MODIS/061/MOD09GQ"),
    ]:
        print(f"Reducing regions for {layer}...")
        t0 = time.perf_counter()
        image: ee.Image = (
            ee.ImageCollection(image_collection_name)
            .filterDate("2023-01-01", "2023-12-31")
            .reduce(reducer=ee.Reducer.mean())
        )

        if layer == "modis":
            image = image.normalizedDifference(
                ["sur_refl_b02_mean", "sur_refl_b01_mean"]
            ).rename("ndvi")

        output_features = reduce_regions(
            image, features, 250 if layer == "modis" else 1000
        )
        print(f"Elapsed time: {time.perf_counter() - t0}")

        print("Writing to file...")
        with open(f"data/{layer}.geojson", "w") as f:
            json.dump({"type": "FeatureCollection", "features": output_features}, f)


if __name__ == "__main__":
    main()
