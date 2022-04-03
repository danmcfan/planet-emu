import os
from dotenv import load_dotenv
from pprint import pprint

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

    pprint(sample_gdf.to_dict(orient="records"))

    assert sample_gdf.shape[0] in [4, 5]
    assert sample_gdf.shape[1] == 8
