from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.task_schema import TaskCreate, TaskOut
from src.tasks.task_service import create_task, get_tasks, update_task, delete_task
from src.database.db import SessionLocal
from src.utils.security import get_current_user
from src.tasks.task_models import Task 

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskOut)
def create(task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_task(db, task.title, task.description, user.id)

@router.get("/all", response_model=list[TaskOut])
def read_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.put("/{task_id}", response_model=TaskOut)
def update(task_id: int, task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = update_task(db, task_id, task.title, task.description, False, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    deleted = delete_task(db, task_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"msg": "Task deleted"}
