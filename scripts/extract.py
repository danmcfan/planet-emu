import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import time

import ee

WORKER_COUNT = 35
SENTINEL = None

WIDTH, HEIGHT, SCALE = 1000, 1000, 250
XMIN, YMIN, XMAX, YMAX = -124.68721, 25.079916, -66.96466, 49.389285


class GridGenerator:
    def __init__(self, scale: int, width: int, height: int):
        self.scale = scale
        self.width = width
        self.height = height

        self.proj = ee.Projection("EPSG:4326").atScale(self.scale).getInfo()

        self.scale_x = self.proj["transform"][0]
        self.scale_y = -self.proj["transform"][4]

        self.crs = self.proj["crs"]

    def create_grids(
        self, xmin: float, ymin: float, xmax: float, ymax: float
    ) -> list[tuple[int, dict]]:
        grids = []
        index = 0
        x = xmin
        y = ymax

        while x < xmax:
            while y > ymin:
                grids.append(
                    (
                        index,
                        {
                            "dimensions": {"width": self.width, "height": self.height},
                            "affineTransform": {
                                "scaleX": self.scale_x,
                                "shearX": 0,
                                "translateX": x,
                                "shearY": 0,
                                "scaleY": self.scale_y,
                                "translateY": y,
                            },
                            "crsCode": self.crs,
                        },
                    )
                )

                y += self.scale_y * self.height
                index += 1

            y = ymax
            x += self.scale_x * self.width

        return grids


def main():
    print("Initializing...")
    credentials = ee.ServiceAccountCredentials(
        "default@ee-danmcfan.iam.gserviceaccount.com", ".private-key.json"
    )
    ee.Initialize(credentials)

    grid_generator = GridGenerator(SCALE, WIDTH, HEIGHT)

    task_queue = queue.Queue()

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

        for index, grid in grid_generator.create_grids(XMIN, YMIN, XMAX, YMAX):
            task_queue.put(
                {"grid": grid, "layer": layer, "index": index, "asset_id": image_id}
            )

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

        for index, grid in grid_generator.create_grids(XMIN, YMIN, XMAX, YMAX):
            task_queue.put(
                {"grid": grid, "layer": layer, "index": index, "expression": image}
            )

    for _ in range(WORKER_COUNT):
        task_queue.put(SENTINEL)

    with ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
        futures = []
        for _ in range(WORKER_COUNT):
            futures.append(executor.submit(worker, task_queue))

        for future in as_completed(futures):
            future.result()


def worker(task_queue: queue.Queue):
    while True:
        item = task_queue.get()

        if item is SENTINEL:
            task_queue.task_done()
            break

        t0 = time.perf_counter()
        print(f"Starting {item['index']} - {item['layer']}...")
        write_geotiff(**item)
        print(f"Finished {item['index']} - {item['layer']}: {time.perf_counter() - t0}")

        task_queue.task_done()


def write_geotiff(
    grid: dict,
    layer: str,
    index: int,
    asset_id: int | None = None,
    expression: ee.Image | None = None,
):
    request = {"fileFormat": "GEO_TIFF", "grid": grid}

    if asset_id:
        request["assetId"] = asset_id
        raw_data = ee.data.getPixels(request)

    if expression:
        request["expression"] = expression
        raw_data = ee.data.computePixels(request)

    os.makedirs(f"data/{layer}")
    with open(f"data/{layer}/{index}.geotiff", "wb") as f:
        f.write(raw_data)


if __name__ == "__main__":
    main()
