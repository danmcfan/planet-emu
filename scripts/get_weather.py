import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
import pandas as pd
import os
import time

from planet_emu import util, gee, image, plot


def main(x: int = 2, y: int = 2, year: int = 2020) -> None:
    if not os.path.isdir(".temp"):
        os.mkdir(".temp")

    NAME = os.getenv("GCP_SERVICE_NAME")
    PROJECT = os.getenv("GCP_PROJECT")

    gee.init(NAME, PROJECT)

    counties_gdf = util.from_pickle("usa_counties")

    for reducer in ["mean", "std", "min", "max"]:
        plot_object = plot.PlanetPlot(
            x=x, y=y, title=f"USA Weather Properties - {reducer.title()}"
        )
        if os.path.isfile(f"data/pickle/weather_{reducer}_{year}.pickle"):
            final_gdf = util.from_pickle(f"weather_{reducer}_{year}")
        else:
            image_collection_object = image.WEATHER_IC
            image_object = image_collection_object.get_reduced_image(
                reducer, f"{year}-01-01", f"{year+1}-01-01"
            )
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

            util.to_pickle(final_gdf, f"weather_{reducer}_{year}")
            util.to_geojson(final_gdf, f"weather_{reducer}_{year}")

        print(f"Plotting {reducer}...")
        final_gdf = final_gdf.loc[
            ~final_gdf["statefp"].isin([2, 15, 60, 66, 69, 72, 78])
        ].copy()

        print(final_gdf.info())

        for index, (column, cmap) in enumerate(
            [
                ("prcp", "Blues"),
                ("srad", "Oranges"),
                ("tmin", "Reds"),
                ("tmax", "Reds"),
            ]
        ):
            print(f"Adding {column} subplot...")
            final_gdf = final_gdf.rename(columns=lambda x: x.replace("_stdDev_", "_"))
            final_gdf[f"{column}_mean"] = pd.to_numeric(final_gdf[f"{column}_mean"])
            plot_object.add_subplot(
                final_gdf,
                f"{column}_mean",
                x=index % x,
                y=index // x,
                title=column,
                legend=True,
                cmap=cmap,
                ticks=False,
            )

        print("Saving to PNG...")
        plot_object.to_png(f"weather_properties_{reducer}", dpi=300)


if __name__ == "__main__":
    main()
