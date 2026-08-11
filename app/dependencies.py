"""Reusable FastAPI dependencies."""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db


def get_task_or_404(task_id: int, db: Session = Depends(get_db)) -> object:
    """Fetch a task by id or raise a 404 HTTPException."""
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task
