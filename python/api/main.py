import database
import schemas
import tasks
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI(
    title="Planet Emu",
    description="An emulator of the planet Earth",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.post("/tasks", response_model=schemas.Task, status_code=201)
def create_task(features: schemas.Features):
    return tasks.invoke_prediction_lambda(features)


@app.get("/tasks/{id}", response_model=schemas.Task)
def read_task(id: str):
    task = database.get_task(id)

    if task is None:
        raise HTTPException(404, "Task not found")

    return task


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: str):
    task = database.get_task(id)

    if task is None:
        raise HTTPException(404, "Task not found")

    database.delete_task(id)


handler = Mangum(app)
