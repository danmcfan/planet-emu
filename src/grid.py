import json

import ee
import shapely


def create_polygons_grid(
    boundary_geojson_filepath: str = "data/input/unitedStates.geojson",
    delta_x: float = 0.1,
    delta_y: float = 0.1,
) -> list[shapely.geometry.Polygon]:
    output_polygons = []

    with open(boundary_geojson_filepath, "r") as f:
        features = json.load(f)["features"]

    polygons = [shapely.geometry.shape(feature["geometry"]) for feature in features]
    boundary = shapely.unary_union(polygons)

    min_x, min_y, max_x, max_y = boundary.bounds

    x = min_x
    y = min_y

    while x < max_x:
        while y < max_y:
            polygon = shapely.geometry.Polygon(
                (
                    (x, y),
                    (x + delta_x, y),
                    (x + delta_x, y + delta_y),
                    (x, y + delta_y),
                    (x, y),
                ),
            )

            if polygon.intersects(boundary):
                output_polygons.append(polygon)
            y += delta_y
        x += delta_x
        y = min_y

    return output_polygons
