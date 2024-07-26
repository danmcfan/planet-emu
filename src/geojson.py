import json

import shapely


def write_polygons_to_geojson_file(
    polygons: list[shapely.geometry.Polygon], filepath: str
):
    features = []

    for index, polygon in enumerate(polygons):
        features.append(
            {
                "type": "Feature",
                "id": index,
                "properties": {},
                "geometry": json.loads(shapely.to_geojson(polygon)),
            }
        )

    with open(filepath, "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
