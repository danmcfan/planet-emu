import logging
import os

import ee
from dotenv import load_dotenv

logger = logging.getLogger("init")


def initialize():
    logger.info("Initializing Earth Engine")

    load_dotenv()

    SERVICE_ACCOUNT = os.environ.get("SERVICE_ACCOUNT")
    PRIVATE_KEY_FILEPATH = os.environ.get("PRIVATE_KEY_FILEPATH")

    ee.Initialize(
        ee.ServiceAccountCredentials(SERVICE_ACCOUNT, PRIVATE_KEY_FILEPATH)
    )


IS_INITIALIZED = False

if not IS_INITIALIZED:
    initialize()
    IS_INITIALIZED = True
