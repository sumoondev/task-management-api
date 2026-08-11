"""Database CRUD operations for the Task model."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def list_tasks(db: Session) -> list[models.Task]:
    """Return all tasks ordered by id ascending."""
    return list(db.scalars(select(models.Task).order_by(models.Task.id)).all())


def get_task(db: Session, task_id: int) -> models.Task | None:
    """Return a single task by id, or None if it does not exist."""
    return db.get(models.Task, task_id)


def create_task(db: Session, payload: schemas.TaskCreate) -> models.Task:
    """Insert a new task and return the persisted instance."""
    task = models.Task(
        title=payload.title.strip(),
        description=payload.description,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(
    db: Session, task: models.Task, payload: schemas.TaskUpdate
) -> models.Task:
    """Replace the mutable fields of an existing task."""
    task.title = payload.title.strip()
    task.description = payload.description
    task.completed = payload.completed
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task) -> None:
    """Remove a task from the database."""
    db.delete(task)
    db.commit()


def mark_completed(db: Session, task: models.Task) -> models.Task:
    """Mark a task as completed."""
    task.completed = True
    db.commit()
    db.refresh(task)
    return task
