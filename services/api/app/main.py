import os
from fastapi import FastAPI
from uuid import uuid4
import redis
import json

app = FastAPI(title="Cloud Native Task Platform")

r = redis.Redis(
    host = os.getenv("REDIS_HOST", "localhost"),
    port = int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

@app.get("/")
def health():
    return {
        "status":"running"
    }

@app.post("/tasks")
def create_task():

    task_id=str(uuid4())

    task={
        "task_id":task_id,
        "status":"queued"
    }

    r.set(task_id, json.dumps(task))
    r.lpush("task_queue", task_id)

    return task

@app.get("/tasks/{task_id}")
def get_task(task_id:str):

    task=r.get(task_id)

    if not task:
        return {"error":"not found"}

    return json.loads(task)