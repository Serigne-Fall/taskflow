from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="TaskFlow")

class Task(BaseModel):
    title: str
    done: bool = False

tasks: dict[int, Task] = {}
next_id = 1

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return [{"id": i, **t.model_dump()} for i, t in tasks.items()]

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global next_id
    tasks[next_id] = task
    next_id += 1
    return {"id": next_id - 1, **task.model_dump()}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
