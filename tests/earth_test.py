from tests.util import GDF
from src import earth


def test_get_mean_image_sample():
    ic_name = earth.IMAGE_COLLECTION_NAMES.get("weather")

    sample_gdf = earth.get_mean_image_sample(
        ic_name,
        GDF,
        year=2020,
        scale=1000,
    )

    assert sample_gdf.shape == (4, 8)
