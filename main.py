import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

with open("data/sample/bulkdens.geojson", "r") as f:
    geojson_data = json.load(f)
    geojson_data = {
        "type": "FeatureCollection",
        "features": geojson_data["features"][:10_000],
    }


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/get-geojson")
async def get_geojson():
    return geojson_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
