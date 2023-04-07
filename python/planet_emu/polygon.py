import os

import geopandas as gpd
from shapely.ops import unary_union


def create_polygon(state_name: str) -> gpd.GeoDataFrame:
    current_folder = os.path.dirname(os.path.abspath(__file__))
    counties_filepath = os.path.join(current_folder, "data/counties.geojson")

    counties: gpd.GeoDataFrame = gpd.read_file(counties_filepath)
    counties = counties.loc[counties["state_name"] == state_name.title()]

    counties = counties.to_crs("EPSG:3857")

    polygons = counties["geometry"].tolist()
    return unary_union(polygons)
