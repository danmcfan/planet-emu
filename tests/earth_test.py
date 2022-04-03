import os
from dotenv import load_dotenv

from tests.util import GDF
from src import earth

load_dotenv()
NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")


def test_get_mean_image_sample():
    earth.init(NAME, PROJECT)

    ic_name = earth.IMAGE_COLLECTION_NAMES.get("weather")

    sample_gdf = earth.get_mean_image_sample(
        ic_name,
        GDF,
        year=2020,
        scale=1000,
    )

    assert sample_gdf.shape == (4, 8)
