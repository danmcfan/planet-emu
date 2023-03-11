import os

import ee

IS_INITIALIZED = False

GCP_SERVICE_NAME = os.getenv("GCP_SERVICE_NAME")
GCP_PROJECT = os.getenv("GCP_PROJECT")
HOME = os.getenv("HOME")

if GCP_SERVICE_NAME is None:
    raise ValueError("GCP_SERVICE_NAME is not set")

if GCP_PROJECT is None:
    raise ValueError("GCP_PROJECT is not set")

if HOME is None:
    raise ValueError("HOME is not set")

SERVICE_ACCOUNT_JSON_FILEPATH = f"{HOME}/secrets/service_account.json"

if not os.path.exists(SERVICE_ACCOUNT_JSON_FILEPATH):
    raise ValueError(
        f"Service account json file does not exist: {SERVICE_ACCOUNT_JSON_FILEPATH}"
    )

service_account = "{}@{}.{}".format(
    GCP_SERVICE_NAME, GCP_PROJECT, "iam.gserviceaccount.com"
)
credentials = ee.ServiceAccountCredentials(
    service_account, SERVICE_ACCOUNT_JSON_FILEPATH
)

if not IS_INITIALIZED:
    ee.Initialize(credentials)  # type: ignore
    IS_INITIALIZED = True
