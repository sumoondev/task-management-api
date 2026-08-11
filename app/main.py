"""FastAPI application entry point for the Task Management API."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db
from app.dependencies import get_task_or_404
from app.models import Task  # noqa: F401  (registers the model with Base)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Management API",
    description=(
        "A small REST API for managing tasks. "
        "Built with FastAPI, SQLAlchemy, and PostgreSQL."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["health"])
def root() -> dict:
    """Sanity-check endpoint."""
    return {"status": "ok"}


@app.post(
    "/tasks",
    response_model=schemas.TaskRead,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
    summary="Create a new task",
)
def create_task(
    payload: schemas.TaskCreate, db: Session = Depends(get_db)
) -> Task:
    """Create a new task from a validated payload."""
    return crud.create_task(db, payload)


@app.get(
    "/tasks",
    response_model=list[schemas.TaskRead],
    tags=["tasks"],
    summary="List all tasks",
)
def read_tasks(db: Session = Depends(get_db)) -> list[Task]:
    """Return every task in the database, ordered by id."""
    return crud.list_tasks(db)


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskRead,
    tags=["tasks"],
    summary="Retrieve a single task",
)
def read_task(task: Task = Depends(get_task_or_404)) -> Task:
    """Return one task by id, or 404 if it does not exist."""
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskRead,
    tags=["tasks"],
    summary="Update an existing task",
)
def update_task_endpoint(
    payload: schemas.TaskUpdate,
    task: Task = Depends(get_task_or_404),
    db: Session = Depends(get_db),
) -> Task:
    """Replace the mutable fields of an existing task."""
    return crud.update_task(db, task, payload)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    summary="Delete a task",
)
def delete_task_endpoint(
    task: Task = Depends(get_task_or_404),
    db: Session = Depends(get_db),
) -> None:
    """Delete a task by id."""
    crud.delete_task(db, task)
    return None


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=schemas.TaskRead,
    tags=["tasks"],
    summary="Mark a task as completed",
)
def complete_task_endpoint(
    task: Task = Depends(get_task_or_404),
    db: Session = Depends(get_db),
) -> Task:
    """Mark the given task as completed."""
    return crud.mark_completed(db, task)
