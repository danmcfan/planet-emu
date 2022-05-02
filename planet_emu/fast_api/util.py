import awswrangler as wr
import pandas as pd
import os
import json

BUCKET = os.getenv("BUCKET")
JSON_DIR = os.getenv("JSON_DIR")


def get_json(basename: str) -> pd.DataFrame:
    path = f"s3://{BUCKET}/{JSON_DIR}/{basename}.json"
    if not wr.s3.does_object_exist(path):
        return pd.DataFrame()
    return wr.s3.read_json(path)


def set_json(df: pd.DataFrame, basename: str) -> None:
    path = f"s3://{BUCKET}/{JSON_DIR}/{basename}.json"
    wr.s3.to_json(df, path)


def remove_json(basename: str) -> None:
    path = f"s3://{BUCKET}/{JSON_DIR}/{basename}.json"
    wr.s3.delete_objects(path)


def to_json(df: pd.DataFrame) -> dict:
    return json.loads(df.to_json(orient="records"))


def get_secret(secret_name: str) -> str:
    return wr.secretsmanager.get_secret_json(secret_name).get("access_token")
