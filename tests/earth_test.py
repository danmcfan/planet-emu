import os
from dotenv import load_dotenv

from tests.util import GDF
from planet_emu.gee import gee

load_dotenv()
NAME = os.getenv("GCP_SERVICE_NAME")
PROJECT = os.getenv("GCP_PROJECT")


def test_get_mean_image_sample():
    gee.init(NAME, PROJECT)

    ic_name = gee.IMAGE_COLLECTION_NAMES.get("weather")

    sample_gdf = gee.get_mean_image_sample(
        ic_name,
        GDF,
        year=2020,
        scale=1000,
    )

    print(sample_gdf)

    assert 0 < sample_gdf.shape[0] < 10
    assert sample_gdf.shape[1] == 8
