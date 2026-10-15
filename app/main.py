from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models import TaskDB

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow")

class Task(BaseModel):
    title: str
    done: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def to_dict(t: TaskDB) -> dict:
    return {"id": t.id, "title": t.title, "done": t.done}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    return [to_dict(t) for t in db.query(TaskDB).all()]

@app.post("/tasks", status_code=201)
def create_task(task: Task, db: Session = Depends(get_db)):
    t = TaskDB(title=task.title, done=task.done)
    db.add(t)
    db.commit()
    db.refresh(t)
    return to_dict(t)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    t = db.get(TaskDB, task_id)
    if t is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(t)
    db.commit()
