from planet_emu import grid_sample as gs
from tests.util import POLYGON

SPLIT = 4
COUNT = SPLIT**2


def test_create_grid_gdf():
    gdf = gs.create_grid_gdf(POLYGON, SPLIT)

    assert gdf.shape == (COUNT, 1)


def test_divide_polygon():
    gdf = gs.divide_polygon(POLYGON, SPLIT)

    assert gdf.shape == (COUNT, 1)
