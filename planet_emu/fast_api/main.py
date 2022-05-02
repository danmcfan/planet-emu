from typing import Dict
from mangum import Mangum
from fastapi import FastAPI, HTTPException
import awswrangler as wr
import pandas as pd
import os
import json

app = FastAPI(
    title="CRUD",
    description="Create Read Update Delete",
    version="0.0.1",
)

BUCKET = os.getenv("BUCKET")
JSON_DIR = os.getenv("JSON_DIR")

def get_json(basename: str) -> pd.DataFrame:
    path = f"s3://{BUCKET}/{JSON_DIR}/{basename}.json"
    if not wr.s3.does_object_exist(path):
        return pd.DataFrame()
    return wr.s3.read_json(path)

def set_json(df: pd.DataFrame, basename: str) -> None:
    path = f"s3://{BUCKET}/{JSON_DIR}/{basename}.json"
    return wr.s3.to_json(df, path)

def to_json(df: pd.DataFrame) -> Dict:
    return json.loads(df.to_json(orient="records"))

@app.get("/")
def index():
    return {
        "message": "Hello World"
    }

@app.get("/mirror/{item}")
def mirror(item: str):
    return {
        "message": item,
    }

@app.get("/get/all")
def get_all():
    df = get_json("items")
    return {
        "data": to_json(df),
    }


@app.get("/add/{item}")
def add_item(item: str):
    df = get_json("items")
    df = df.append({"item": item}, ignore_index=True)
    set_json(df, "items")
    return {
        "message": f"Added {item} to the list",
        "item": item,
    }

@app.get("/soil/get/{layer}/{code}")
def get_soil(layer: str, code: int):
    if code < 100:
        df = pd.read_sql()
    else:
        data = get_soil_json(layer, code, "county")
    return data


handler = Mangum(app)