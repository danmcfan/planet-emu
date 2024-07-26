import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/tiles/{z}/{x}/{y}.pbf")
async def get_tile(z: int, x: int, y: int):
    tile_path = os.path.join("tiles", str(z), str(x), f"{y}.pbf")
    if os.path.exists(tile_path):
        return FileResponse(
            tile_path,
            media_type="application/x-protobuf",
            headers={"Content-Encoding": "gzip"},
        )
    else:
        raise HTTPException(status_code=404, detail="Tile not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
