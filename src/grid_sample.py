import geopandas as gpd
import numpy as np
from shapely import geometry


def get_grid_gdf(
    min_x: float, min_y: float, max_x: float, max_y: float, split: int = 2
) -> gpd.GeoDataFrame:
    x_list = np.linspace(min_x, max_x, split + 1)
    y_list = np.linspace(min_y, max_y, split + 1)

    rectangles = []
    for i in range(len(x_list) - 1):
        for j in range(len(y_list) - 1):
            rectangles.append(
                geometry.box(
                    x_list[i], y_list[j], x_list[i + 1], y_list[j + 1]
                )
            )

    gdf = gpd.GeoDataFrame(geometry=rectangles, crs="EPSG:4326")
    return gdf


def divide_polygon(
    polygon: geometry.Polygon, split: int = 2
) -> gpd.GeoDataFrame:
    min_x, min_y, max_x, max_y = polygon.bounds

    grid_gdf = get_grid_gdf(min_x, min_y, max_x, max_y, split)

    polygon_gdf = gpd.GeoDataFrame(
        geometry=grid_gdf.intersection(polygon), crs="EPSG:4326"
    )
    polygon_gdf = polygon_gdf.loc[~polygon_gdf.geometry.is_empty]

    return polygon_gdf
