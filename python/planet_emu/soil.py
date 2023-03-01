import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
import pandas as pd

from planet_emu import util

LAYER_NAMES = [
    "bulkdens",
    "clay",
    "ph",
    "sand",
    "soc",
    "swc",
]


def filter_cols(
    in_df: pd.DataFrame, layer_name: str, index_cols: list[str]
) -> pd.DataFrame:
    soil_cols = index_cols + [c for c in in_df.columns if c.startswith("b")]
    out_df = in_df[soil_cols].copy()
    out_df.columns = [c.replace("b", f"{layer_name}_") for c in out_df.columns]
    return out_df


def clean_soil_layer(in_gdf: gpd.GeoDataFrame, layer_name: str) -> pd.DataFrame:
    out_df = in_gdf.rename(columns={"geoid": "fips_code"})
    out_df = filter_cols(out_df, layer_name, ["fips_code"])
    return out_df


def export_soil_counties() -> None:
    counties = util.from_geojson("counties")
    for layer_name in LAYER_NAMES:
        soil_gdf = util.from_geojson(layer_name)
        soil_df = clean_soil_layer(soil_gdf, layer_name)
        counties = counties.merge(soil_df, on="fips_code", how="left")
    util.to_geojson(counties, "soil_counties")
