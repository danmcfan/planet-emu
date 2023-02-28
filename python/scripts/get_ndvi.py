import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
import os
import time

from planet_emu import util, gee, image


def main(year: int = 2020) -> None:
    NAME = os.getenv("GCP_SERVICE_NAME")
    PROJECT = os.getenv("GCP_PROJECT")

    gee.init(NAME, PROJECT)

    counties_gdf = util.from_geojson("counties")

    image_collection_object = image.MODIS_IC
    image_object = image_collection_object.get_reduced_image(
        "mean", f"{year}-01-01", f"{year+1}-01-01"
    )
    image_object.set_ndvi()
    final_gdf = gpd.GeoDataFrame()
    for state_name in counties_gdf["state_name"].sort_values().unique():
        t0 = time.perf_counter()
        result_gdf = image_object.reduce_regions(
            counties_gdf.loc[counties_gdf["state_name"] == state_name]
        )
        final_gdf = final_gdf.append(result_gdf, ignore_index=True)
        print(
            f"STATE_NAME={state_name}",
            f"YEAR={year}",
            f"TIME={int(time.perf_counter() - t0)}s",
        )
    final_gdf["year"] = year
    util.to_geojson(final_gdf, f"ndvi_{year}")


if __name__ == "__main__":
    main()
