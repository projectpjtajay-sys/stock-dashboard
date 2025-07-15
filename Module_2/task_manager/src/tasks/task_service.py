from sqlalchemy.orm import Session
from src.tasks.task_models import Task
from src.notifications.websocket_manager import manager
import asyncio


def create_task(db: Session, title: str, description: str, user_id: int):
    task = Task(title=title, description=description, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)

    # Send real-time notification (safe from sync context)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    asyncio.run_coroutine_threadsafe(
        manager.send_personal_message(str(user_id), f"Task Created: {task.title}"),
        loop
    )

    return task


def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


def update_task(
    db: Session,
    task_id: int,
    title: str,
    description: str,
    completed: bool,
    user_id: int
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.title = title
        task.description = description
        task.completed = completed
        db.commit()
        db.refresh(task)

        # Safe WebSocket notification
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        asyncio.run_coroutine_threadsafe(
            manager.send_personal_message(str(user_id), f"Task Updated: {task.title}"),
            loop
        )

    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        db.delete(task)
        db.commit()

        # Safe WebSocket notification
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        asyncio.run_coroutine_threadsafe(
            manager.send_personal_message(str(user_id), f"🗑️ Task Deleted: ID {task_id}"),
            loop
        )

    return task
