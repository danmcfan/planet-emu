from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from uuid import uuid4

from planet_emu.fast_api import util


class Point(BaseModel):
    x: float
    y: float


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
        "message": "Go to https://api.planet-emu.com/docs for complete API documentation."
    }


@app.post("/submit/")
def submit_job(point: Point):
    if not (-124.763068 <= point.x <= -66.949895):
        return {"point": point, "error": "X coordinate is out of range"}
    if not (24.523096 <= point.y <= 49.384358):
        return {"point": point, "error": "Y coordinate is out of range"}

    job_id = uuid4().hex[:8]

    data = util.invoke_job(point.x, point.y, job_id)

    return data


@app.post("/status/{job_id}")
def get_status(job_id: str):
    data = util.get_json(job_id)

    if not data:
        raise HTTPException(400, "Job not found")

    return {
        "job_id": job_id,
        "status": data[0]["status"],
    }


@app.get("/results/{job_id}")
def get_results(job_id: str):
    data = util.get_json(job_id)

    if not data:
        raise HTTPException(400, "Job not found")

    if data[0]["status"] == "pending":
        raise HTTPException(400, "Job is still pending")

    return {
        "job_id": job_id,
        "data": data[0],
    }


handler = Mangum(app)
