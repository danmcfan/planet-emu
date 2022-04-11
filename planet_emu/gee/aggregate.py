import warnings

warnings.simplefilter("ignore", FutureWarning)

import os
import time
import ee
import eeconvert
from dotenv import load_dotenv

from planet_emu import util, gee, grid_sample

load_dotenv()

NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")

gee.init(NAME, PROJECT)

counties = util.from_pickle("usa_counties")

states = (
    counties[["statefp", "geometry"]]
    .dissolve(by="statefp")
    .reset_index()
    .copy()
)

illinois = counties.loc[counties["statefp"] == 17].dissolve().copy()

for ic_name, label in [("NASA/ORNL/DAYMET_V4", "weather")]:
    for split in [
        70,
        71,
        72,
        73,
        74,
        75,
    ]:
        t0 = time.perf_counter()

        in_gdf = grid_sample.divide_polygon(illinois.iloc[0].geometry, split)
        in_fc = eeconvert.gdfToFc(in_gdf)

        image = (
            ee.ImageCollection(ic_name)
            .filterDate("2020-01-01", "2020-02-01")
            .filterBounds(in_fc)
            .mean()
        )

        out_fc = image.reduceRegions(
            in_fc,
            reducer=ee.Reducer.mean()
            .combine(ee.Reducer.stdDev(), sharedInputs=True)
            .combine(ee.Reducer.min(), sharedInputs=True)
            .combine(ee.Reducer.max(), sharedInputs=True)
            .combine(ee.Reducer.sum(), sharedInputs=True),
            crs=ee.Projection("EPSG:4326"),
            scale=1000,
        )
        out_gdf = eeconvert.fcToGdf(out_fc)

        td = time.perf_counter() - t0
        print(td)

        basename = f"{label}_illinois_y2020_m1_s{split}"
        util.to_pickle(out_gdf, basename, temp=True)
        util.to_geojson(out_gdf, basename, temp=True)
        util.to_csv(out_gdf, basename, temp=True)
