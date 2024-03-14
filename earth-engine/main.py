import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("main")

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

from src.grid import divide_polygon
from src.image import ImageAsset, create_image, reduce_regions, sample_regions


def main():
    logger.info("Creating image")
    image = create_image(ImageAsset.BULK_DENSITY)

    logger.info("Dividing polygon")
    gdf = divide_polygon(
        Polygon(
            [
                (-124.4096, 41.9983),
                (-120.0029, 41.9983),
                (-117.9561, 37.5172),
                (-116.3217, 33.0744),
                (-118.4143, 33.0744),
                (-120.4968, 34.9792),
                (-122.5793, 37.2171),
                (-124.4096, 40.0124),
                (-124.4096, 41.9983),
            ]
        ),
        resolution=1,
    )

    fig, ax = plt.subplots()
    gdf.plot(edgecolor="black", facecolor="none", ax=ax)

    gdf.to_file("data/grid.geojson", driver="GeoJSON")
    fig.savefig("data/grid.png", dpi=1000)

    logger.info("Reducing regions")
    reduce_gdf = reduce_regions(image, gdf)

    fig, ax = plt.subplots()
    reduce_gdf.plot(column="b0", legend=True, ax=ax)

    reduce_gdf.to_file("data/reduce.geojson", driver="GeoJSON")
    fig.savefig("data/reduce.png", dpi=1000)

    for i in range(len((gdf))):
        logger.info(f"Sampling regions for square {i+1} / {len(gdf)}")
        square_gdf = gdf.iloc[i : i + 1]
        sample_gdf = sample_regions(image, square_gdf)

        fig, ax = plt.subplots()
        sample_gdf.plot(column="b0", legend=True, markersize=1, ax=ax)

        sample_gdf.to_file(f"data/sample_{i}.geojson", driver="GeoJSON")
        fig.savefig(f"data/sample_{i}.png", dpi=1000)


if __name__ == "__main__":
    main()
