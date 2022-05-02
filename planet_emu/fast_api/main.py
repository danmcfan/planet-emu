from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import util

app = FastAPI(
    title="planet-emu",
    description="Backend Planet Emulator",
    version="0.1.0",
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
    return {"message": "index"}


@app.get("/mapbox/access-token")
def access_token():
    return {"access_token": util.get_secret("mapbox")}


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
