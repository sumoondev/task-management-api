"""FastAPI application entry point for the Task Management API."""

from fastapi import FastAPI

app = FastAPI(
    title="Task Management API",
    description="A simple REST API for managing tasks.",
    version="0.1.0",
)


@app.get("/", tags=["health"])
def root() -> dict:
    """Root endpoint for sanity checks."""
    return {"status": "ok"}
