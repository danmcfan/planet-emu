from shapely import geometry
from matplotlib import pyplot as plt

from src import grid_sample as gs

EXPORT = False
SPLIT = 4
COUNT = SPLIT**2


def test_get_grid_gdf():
    gdf = gs.get_grid_gdf(-95, 35, 85, 45, SPLIT)
    gdf.plot(facecolor="none", edgecolor="black")

    if EXPORT:
        gdf.to_csv(".temp/grid.csv")
        plt.savefig(".temp/grid.png")

    assert gdf.shape == (COUNT, 1)


def test_divide_polygon():
    centroid = geometry.Point([-90, 40])
    polygon = centroid.buffer(0.01)

    gdf = gs.divide_polygon(polygon, SPLIT)
    gdf.plot(facecolor="none", edgecolor="black")

    if EXPORT:
        gdf.to_csv(".temp/divide.csv")
        plt.savefig(".temp/divide.png")

    assert gdf.shape == (COUNT, 1)
