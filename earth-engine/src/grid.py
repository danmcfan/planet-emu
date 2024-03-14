import geopandas as gpd
from shapely import geometry


def divide_polygon(
    polygon: geometry.Polygon, resolution: float, crs="EPSG:4326"
) -> gpd.GeoDataFrame:
    grid_gdf = create_grid_gdf(polygon, resolution, crs)

    polygon_gdf = gpd.GeoDataFrame(
        geometry=grid_gdf.intersection(polygon), crs=crs
    )
    polygon_gdf = polygon_gdf.loc[~polygon_gdf.geometry.is_empty].reset_index(
        drop=True
    )

    return polygon_gdf


def create_grid_gdf(
    polygon: geometry.Polygon, resolution: float, crs="EPSG:4326"
) -> gpd.GeoDataFrame:
    min_x, min_y, max_x, max_y = polygon.bounds

    rectangles = []

    x = min_x
    y = min_y

    while x < max_x:
        while y < max_y:
            rectangles.append(
                geometry.box(x, y, x + resolution, y + resolution)
            )
            y += resolution
        x += resolution
        y = min_y

    return gpd.GeoDataFrame(geometry=rectangles, crs=crs)
