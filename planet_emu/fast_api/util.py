import awswrangler as wr
import pandas as pd
import os
import json

BUCKET = os.getenv("BUCKET")
JSON_DIR = os.getenv("JSON_DIR")


def get_path(basename: str, ext: str = "json") -> str:
    return f"s3://{BUCKET}/{JSON_DIR}/{basename}.{ext}"


def get_json(basename: str) -> dict:
    path = get_path(basename)
    if not wr.s3.does_object_exist(path):
        return dict()
    df = wr.s3.read_json(path)
    return df.to_dict(orient="records")


def set_json(records: list[dict], basename: str) -> None:
    path = get_path(basename)
    df = pd.DataFrame(records)
    wr.s3.to_json(df, path)


def del_json(basename: str) -> None:
    path = get_path(basename)
    wr.s3.delete_objects(path)
