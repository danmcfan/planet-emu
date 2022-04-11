import geopandas as gpd
import numpy as np
from shapely import geometry


def create_grid_gdf(
    polygon: geometry.Polygon, split: int = 2
) -> gpd.GeoDataFrame:
    min_x, min_y, max_x, max_y = polygon.bounds

    x_list = np.linspace(min_x, max_x, split + 1)
    y_list = np.linspace(min_y, max_y, split + 1)

    rectangles = [
        geometry.box(
            x_list[i],
            y_list[j],
            x_list[i + 1],
            y_list[j + 1],
        )
        for i in range(split)
        for j in range(split)
    ]

    return gpd.GeoDataFrame(geometry=rectangles, crs="EPSG:4326")


def divide_polygon(
    polygon: geometry.Polygon, split: int = 2
) -> gpd.GeoDataFrame:
    grid_gdf = create_grid_gdf(polygon, split)

    polygon_gdf = gpd.GeoDataFrame(
        geometry=grid_gdf.intersection(polygon), crs="EPSG:4326"
    )
    polygon_gdf = polygon_gdf.loc[~polygon_gdf.geometry.is_empty].reset_index(
        drop=True
    )

    return polygon_gdf
