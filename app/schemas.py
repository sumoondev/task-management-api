"""Pydantic schemas for request validation and response serialization."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

class TaskBase(BaseModel):
    """Fields shared by create and update operations."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short title of the task (1-200 characters).",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional long-form description of the task.",
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return value 

class TaskUpdate(BaseModel):
    """Schema for fully updating an existing task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = False
class TaskComplete(BaseModel):
    """Schema for the PATCH /complete endpoint response payload."""


    completed: bool
class TaskRead(TaskBase):
    """Schema for serializing a task in API responses."""
    id: int
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

