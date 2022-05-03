import warnings

warnings.simplefilter("ignore", FutureWarning)

import geopandas as gpd
import pandas as pd

LAYER_NAMES = [
    "bulkdens",
    "clay",
    "ph",
    "sand",
    "soc",
    "swc",
]


def filter_means(
    in_df: pd.DataFrame, layer_name: str, index_cols: list[str]
) -> pd.DataFrame:
    mean_cols = index_cols + [c for c in in_df.columns if "mean" in c]
    out_df = in_df[mean_cols].copy()
    out_df.columns = [c.replace("mean", layer_name) for c in out_df.columns]
    return out_df


def clean_soil_layer(in_gdf: gpd.GeoDataFrame, layer_name: str) -> pd.DataFrame:
    out_df = in_gdf.rename(columns={"geoid": "fips_code"})
    out_df = filter_means(out_df, layer_name, ["fips_code"])
    return out_df


def export_soil_counties() -> None:
    counties = gpd.read_file("./data/geojson/counties.geojson")
    for layer_name in LAYER_NAMES:
        soil_gdf = gpd.read_file(f"./data/geojson/{layer_name}.geojson")
        soil_df = clean_soil_layer(soil_gdf, layer_name)
        counties = counties.merge(soil_df, on="fips_code", how="left")
    counties.to_file("./data/geojson/soil_counties.geojson")
