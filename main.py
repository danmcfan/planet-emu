import json
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Load the GeoJSON data
with open("data/sample/bulkdens.geojson", "r") as f:
    geojson_data = json.load(f)


MIN_ZOOM_LEVEL = 6  # Adjusted minimum zoom level


def wrap_longitude(lon):
    return ((lon + 180) % 360) - 180


def filter_features(bounds: list[float], zoom: int):
    if zoom < MIN_ZOOM_LEVEL:
        return []

    xmin, ymin, xmax, ymax = bounds

    return [
        feature
        for feature in geojson_data["features"]
        if xmin <= feature["geometry"]["coordinates"][0][0][0] <= xmax
        and ymin <= wrap_longitude(feature["geometry"]["coordinates"][0][0][1]) <= ymax
    ]


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/geojson")
async def get_geojson(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    zoom: int,
):
    # Validate latitude bounds
    if not (-90 <= ymin <= 90) or not (-90 <= ymax <= 90):
        raise HTTPException(status_code=400, detail="Invalid latitude values")

    # Wrap longitude values
    xmin = wrap_longitude(xmin)
    xmax = wrap_longitude(xmax)

    print(xmin, ymin, xmax, ymax, zoom)
    filtered_features = filter_features([xmin, ymin, xmax, ymax], zoom)
    return {"type": "FeatureCollection", "features": filtered_features}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
