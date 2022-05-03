import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
import os
import time

from planet_emu import util, gee, image, plot


def main(year: int = 2020) -> None:
    if not os.path.isdir(".temp"):
        os.mkdir(".temp")

    NAME = os.getenv("GCP_SERVICE_NAME")
    PROJECT = os.getenv("GCP_PROJECT")

    gee.init(NAME, PROJECT)

    counties_gdf = util.from_pickle("usa_counties")

    for reducer in ["mean", "std", "min", "max"]:
        image_collection_object = image.SENTINEL_IC
        image_collection_object.scale = 1000
        image_object = image_collection_object.get_reduced_image(
            reducer, f"{year}-01-01", f"{year+1}-01-01"
        )
        image_object.set_ndvi()
        final_gdf = gpd.GeoDataFrame()
        for statefp in counties_gdf["statefp"].sort_values().unique():
            t0 = time.perf_counter()
            result_gdf = image_object.reduce_regions(
                counties_gdf.loc[counties_gdf["statefp"] == statefp]
            )
            final_gdf = final_gdf.append(result_gdf, ignore_index=True)
            print(
                f"STATEFP={statefp}",
                f"REDUCER={reducer}",
                f"YEAR={year}",
                f"TIME={int(time.perf_counter() - t0)}s",
            )

        util.to_pickle(final_gdf, f"sentinel_{reducer}_{year}")
        util.to_geojson(final_gdf, f"sentinel_{reducer}_{year}")


if __name__ == "__main__":
    main()
