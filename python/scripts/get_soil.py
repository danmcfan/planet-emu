import warnings

warnings.simplefilter("ignore", FutureWarning)

import os
import time

import geopandas as gpd

from planet_emu import gee, image, util


def main() -> None:
    NAME = os.getenv("GCP_SERVICE_NAME")
    PROJECT = os.getenv("GCP_PROJECT")

    gee.init(NAME, PROJECT)

    counties_gdf = util.from_geojson("counties")

    for image_object, name in [
        (image.BULKDENS_IMG, "bulkdens"),
        (image.CLAY_IMG, "clay"),
        (image.SOC_IMG, "soc"),
        (image.PH_IMG, "ph"),
        (image.SAND_IMG, "sand"),
        (image.SWC_IMG, "swc"),
    ]:
        if os.path.isfile(f"data/geojson/{name}.geojson"):
            final_gdf = util.from_geojson(name)
        else:
            final_gdf = gpd.GeoDataFrame()
            for state_name in counties_gdf["state_name"].sort_values().unique():
                t0 = time.perf_counter()
                result_gdf = image_object.reduce_regions(
                    counties_gdf.loc[counties_gdf["state_name"] == state_name]
                )
                final_gdf = final_gdf.append(result_gdf, ignore_index=True)
                print(
                    f"STATE_NAME={state_name}",
                    f"IMAGE={name}",
                    f"TIME={int(time.perf_counter() - t0)}s",
                )

            util.to_geojson(final_gdf, name)


if __name__ == "__main__":
    main()
