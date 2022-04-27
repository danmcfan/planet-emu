import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
from dotenv import load_dotenv
import os
import time

from planet_emu import util, gee, image, plot


def main(x: int = 3, y: int = 2, depth: int = 0) -> None:
    if not os.path.isdir(".temp"):
        os.mkdir(".temp")

    load_dotenv()

    NAME = os.getenv("GCP_SERVICE_NAME")
    PROJECT = os.getenv("GCP_PROJECT")

    gee.init(NAME, PROJECT)

    counties_gdf = util.from_pickle("usa_counties")

    plot_object = plot.PlanetPlot(
        x=x, y=y, title=f"USA Soil Properties - {depth} cm Depth"
    )
    for index, (image_object, name, cmap) in enumerate(
        [
            (image.BULKDENS_IMG, "bulkdens", "Purples"),
            (image.CLAY_IMG, "clay", "Reds"),
            (image.SOC_IMG, "soc", "Greys"),
            (image.PH_IMG, "ph", "Greens"),
            (image.SAND_IMG, "sand", "Oranges"),
            (image.SWC_IMG, "swc", "Blues"),
        ]
    ):
        if os.path.isfile(f"data/pickle/{name}.pickle"):
            final_gdf = util.from_pickle(name)
        else:
            final_gdf = gpd.GeoDataFrame()
            for statefp in counties_gdf["statefp"].sort_values().unique():
                t0 = time.perf_counter()
                result_gdf = image_object.reduce_regions(
                    counties_gdf.loc[counties_gdf["statefp"] == statefp]
                )
                final_gdf = final_gdf.append(result_gdf, ignore_index=True)
                print(
                    f"STATEFP={statefp})",
                    f"IMAGE={name}",
                    f"TIME={int(time.perf_counter() - t0)}s",
                )

            util.to_pickle(final_gdf, name)
            util.to_geojson(final_gdf, name)

        print(f"Plotting {name}...")
        final_gdf = final_gdf.loc[
            ~final_gdf["statefp"].isin([2, 15, 60, 66, 69, 72, 78])
        ].copy()
        plot_object.add_subplot(
            final_gdf,
            f"b{depth}_mean",
            x=index % x,
            y=index // x,
            title=name,
            legend=True,
            cmap=cmap,
            ticks=False,
        )

    print("Saving to PNG...")
    plot_object.to_png(f"soil_properties_{depth}cm", dpi=300)


if __name__ == "__main__":
    for depth in [0, 10, 30, 60, 100, 200]:
        main(depth=depth)
