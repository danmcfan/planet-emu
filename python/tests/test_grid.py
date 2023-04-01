from tests.util import POLYGON

from python.planet_emu import grid as gs

SPLIT = 4
COUNT = SPLIT**2


def test_create_grid_gdf():
    gdf = gs.create_grid_gdf(POLYGON, SPLIT)

    assert gdf.shape == (COUNT, 1)


def test_divide_polygon():
    gdf = gs.divide_polygon(POLYGON, SPLIT)

    assert gdf.shape == (COUNT, 1)
