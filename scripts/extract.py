import os
import logging
import queue
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import click
import ee

from src.grid import GridGenerator

SENTINEL = None

logger = logging.getLogger(__name__)


@click.command()
@click.option("--workers", default=35, help="Number of parallel workers to run")
@click.option("--width", default=1000, help="Width of raster tile in pixels")
@click.option("--height", default=1000, help="Height of raster tile in pixels")
@click.option("--scale", default=500, help="Scale of raster tile in meters")
@click.option("--xmin", default=-124.68721, help="X coordinate minimum in degrees")
@click.option("--ymin", default=25.079916, help="X coordinate minimum in degrees")
@click.option("--xmax", default=-66.96466, help="X coordinate minimum in degrees")
@click.option("--ymax", default=49.389285, help="X coordinate minimum in degrees")
@click.option(
    "--start_date", default="2023-01-01", help="Start date for image collection filter"
)
@click.option(
    "--end_date", default="2023-12-31", help="End date for image collection filter"
)
@click.option("--output_dir", default="data", help="Output directory")
def main(
    workers: int,
    width: int,
    height: int,
    scale: int,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    start_date: str,
    end_date: str,
    output_dir: str,
):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    email = os.getenv("GEE_EMAIL", "default@ee-danmcfan.iam.gserviceaccount.com")
    key_file = os.getenv("GEE_KEY_FILE", ".private-key.json")

    logger.info("Initializing Google Earth Engine...")
    credentials = ee.ServiceAccountCredentials(email, key_file)
    ee.Initialize(credentials)

    grid_generator = GridGenerator(scale, width, height)
    grids = grid_generator.create_grids(xmin, ymin, xmax, ymax)

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

        for index, grid in grids:
            task_queue.put(
                {"grid": grid, "layer": layer, "index": index, "asset_id": image_id}
            )

    for layer, image_collection_name in [
        ("daymet", "NASA/ORNL/DAYMET_V4"),
        ("landsat", "LANDSAT/LC09/C02/T1_L2"),
    ]:
        image = (
            ee.ImageCollection(image_collection_name)
            .filterDate(start_date, end_date)
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

        for index, grid in grids:
            task_queue.put(
                {"grid": grid, "layer": layer, "index": index, "expression": image}
            )

    for _ in range(workers):
        task_queue.put(SENTINEL)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for _ in range(workers):
            futures.append(executor.submit(worker, output_dir, task_queue))

        for future in as_completed(futures):
            future.result()


def worker(output_dir: str, task_queue: queue.Queue):
    while True:
        item = task_queue.get()

        if item is SENTINEL:
            task_queue.task_done()
            break

        start_time = time.perf_counter()
        logger.info(f"Starting extraction ({item['layer']}-{item['index']})...")
        write_data(output_dir=output_dir, **item)
        elapsed_time = time.perf_counter() - start_time
        logger.info(
            f"Completed extraction ({item['layer']}-{item['index']}): {elapsed_time:.2f}s"
        )

        task_queue.task_done()


def write_data(
    output_dir: str,
    grid: dict,
    layer: str,
    index: int,
    asset_id: int | None = None,
    expression: ee.Image | None = None,
):
    request = {"fileFormat": "NPY", "grid": grid}

    if asset_id:
        request["assetId"] = asset_id
        raw_data = ee.data.getPixels(request)

    if expression:
        request["expression"] = expression
        raw_data = ee.data.computePixels(request)

    os.makedirs(f"{output_dir}/{layer}", exist_ok=True)
    with open(f"{output_dir}/{layer}/{index}.npy", "wb") as f:
        f.write(raw_data)


if __name__ == "__main__":
    main()
