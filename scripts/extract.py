import time

import ee


def main():
    print("Initializing...")
    credentials = ee.ServiceAccountCredentials(
        "default@ee-danmcfan.iam.gserviceaccount.com", ".private-key.json"
    )
    ee.Initialize(credentials)

    width, height, scale = 1000, 1000, 1000

    # Make a projection to discover the scale in degrees.
    proj = ee.Projection("EPSG:4326").atScale(scale).getInfo()

    # Get scales out of the transform.
    scale_x = proj["transform"][0]
    scale_y = -proj["transform"][4]

    xmin, ymin, xmax, ymax = -124.68721, 25.079916, -66.96466, 49.389285

    x = xmin
    y = ymax
    grid_index = 0

    while x < xmax:
        while y > ymin:
            print(grid_index, x, y)

            grid = {
                "dimensions": {"width": width, "height": height},
                "affineTransform": {
                    "scaleX": scale_x,
                    "shearX": 0,
                    "translateX": x,
                    "shearY": 0,
                    "scaleY": scale_y,
                    "translateY": y,
                },
                "crsCode": proj["crs"],
            }

            for layer, image_name in [
                ("bulkdens", "OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02"),
                ("clay", "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02"),
                ("ocarbon", "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02"),
                ("ph", "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02"),
                ("sand", "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02"),
                ("water", "OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01"),
            ]:
                image = ee.Image(image_name)
                image_id = image.getInfo()["id"]

                # Make a request object.
                request = {"assetId": image_id, "fileFormat": "GEO_TIFF", "grid": grid}

                t0 = time.perf_counter()
                image_png = ee.data.getPixels(request)
                print(f"Elapsed time: {time.perf_counter() - t0}")

                with open(f"data/{layer}/{grid_index}.geotiff", "wb") as f:
                    f.write(image_png)

            for layer, image_collection_name in [
                ("daymet", "NASA/ORNL/DAYMET_V4"),
                ("landsat", "LANDSAT/LC09/C02/T1_L2"),
            ]:
                image = (
                    ee.ImageCollection(image_collection_name)
                    .filterDate("2023-01-01", "2023-12-31")
                    .mean()
                )
                if layer == "landsat":
                    image = image.expression(
                        "(NIR - RED) / (NIR + RED)",
                        {
                            "NIR": image.select("SR_B5"),
                            "RED": image.select("SR_B4"),
                        },
                    )

                request = {"expression": image, "fileFormat": "GEO_TIFF", "grid": grid}

                t0 = time.perf_counter()
                image_png = ee.data.computePixels(request)
                print(f"Elapsed time: {time.perf_counter() - t0}")

                with open(f"data/{layer}/{grid_index}.geotiff", "wb") as f:
                    f.write(image_png)

            y += scale_y * height
            grid_index += 1

        y = ymax
        x += scale_x * width


if __name__ == "__main__":
    main()
