"""Unit tests for Pydantic schema validation."""

import pytest
from pydantic import ValidationError

from app.schemas import TaskCreate, TaskUpdate


class TestTaskCreateValidation:
    """Validation rules for the create-task payload."""

    def test_valid_payload_is_accepted(self) -> None:
        task = TaskCreate(title="Buy milk", description="2L semi-skimmed")
        assert task.title == "Buy milk"
        assert task.description == "2L semi-skimmed"
        assert task.completed is False

    def test_title_is_required(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate()  # type: ignore[call-arg]

    def test_empty_title_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_whitespace_title_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate(title="   ")

    def test_oversized_title_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 201)

    def test_oversized_description_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TaskCreate(title="Valid", description="x" * 1001)


class TestTaskUpdateValidation:
    """Validation rules for the update-task payload."""

    def test_defaults(self) -> None:
        payload = TaskUpdate(title="Updated")
        assert payload.completed is False
        assert payload.description is None
