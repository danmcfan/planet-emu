from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import util
from models import Item

app = FastAPI(
    title="planet-emu-api",
    description="Planet Emulator API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://danmcfan.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {
        "message": "Go to https://api.planet-emu.com/docs for complete documentation on the API."
    }


@app.get("/geojson/counties")
def get_counties_geojson():
    return util.get_json("counties")


@app.post("/items/")
def create_item(item: Item):
    return item


@app.get("/mirror/{item}")
def mirror(item: str):
    return {
        "message": item,
    }


@app.get("/add/{item}")
def add_item(item: str):
    df = util.get_json("items")
    df = df.append({"item": item}, ignore_index=True)
    util.set_json(df, "items")
    return {
        "message": f"Added {item}",
        "item": item,
    }


@app.get("/get/items")
def get_items():
    df = util.get_json("items")
    return {
        "data": util.to_json(df),
    }


@app.get("/delete/items")
def delete_items():
    util.remove_json("items")
    return {
        "message": "Deleted all items",
    }


handler = Mangum(app)
