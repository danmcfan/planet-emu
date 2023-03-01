import random

import geopandas as gpd
from shapely import geometry

CENTROID = geometry.Point(
    random.uniform(-100, -80),
    random.uniform(30, 50),
)

POLYGON = CENTROID.buffer(0.01)

GDF = gpd.GeoDataFrame(geometry=[POLYGON], crs="EPSG:4326")
