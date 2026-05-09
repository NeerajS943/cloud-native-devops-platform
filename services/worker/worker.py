import os
import redis
import json
import time

r = redis.Redis(
    host = os.getenv("REDIS_HOST", "localhost"),
    port = int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

print("Worker started...",flush=True)

while True:

    job = r.brpop("task_queue", timeout=5)

    if job:

        task_id = job[1]

        print(f"Processing task {task_id}")

        time.sleep(5)

        task = {
            "task_id": task_id,
            "status":"completed"
        }

        r.set(
            task_id,
            json.dumps(task)
        )

        print(f"Completed {task_id}")