from tests.util import POLYGON

from earth import grid

SPLIT = 4
COUNT = SPLIT**2


def test_create_grid_gdf():
    gdf = grid.create_grid_gdf(POLYGON, SPLIT)

    assert gdf.shape == (COUNT, 1)


def test_divide_polygon():
    gdf = grid.divide_polygon(POLYGON, SPLIT)

    assert gdf.shape == (COUNT, 1)
