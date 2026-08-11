"""Integration tests for the Task Management API endpoints."""

import pytest


@pytest.fixture()
def sample_payload() -> dict:
    return {"title": "Write README", "description": "Make it useful"}


class TestCreateTask:
    def test_creates_task_and_returns_201(self, client, sample_payload) -> None:
        response = client.post("/tasks", json=sample_payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_payload["title"]
        assert data["completed"] is False
        assert "id" in data and "created_at" in data

    def test_rejects_empty_title_with_422(self, client) -> None:
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422


class TestListTasks:
    def test_returns_empty_list_initially(self, client) -> None:
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_created_tasks(self, client, sample_payload) -> None:
        client.post("/tasks", json=sample_payload)
        client.post("/tasks", json={"title": "Second"})
        response = client.get("/tasks")
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2
        assert {t["title"] for t in body} == {"Write README", "Second"}


class TestRetrieveTask:
    def test_returns_404_for_missing_task(self, client) -> None:
        response = client.get("/tasks/9999")
        assert response.status_code == 404

    def test_returns_existing_task(self, client, sample_payload) -> None:
        created = client.post("/tasks", json=sample_payload).json()
        response = client.get(f"/tasks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]


class TestUpdateTask:
    def test_updates_existing_task(self, client, sample_payload) -> None:
        created = client.post("/tasks", json=sample_payload).json()
        response = client.put(
            f"/tasks/{created['id']}",
            json={"title": "Updated title", "description": "New desc", "completed": True},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated title"
        assert body["completed"] is True

    def test_update_missing_task_returns_404(self, client) -> None:
        response = client.put(
            "/tasks/9999",
            json={"title": "x", "description": None, "completed": False},
        )
        assert response.status_code == 404


class TestDeleteTask:
    def test_deletes_existing_task(self, client, sample_payload) -> None:
        created = client.post("/tasks", json=sample_payload).json()
        response = client.delete(f"/tasks/{created['id']}")
        assert response.status_code == 204
        assert client.get(f"/tasks/{created['id']}").status_code == 404

    def test_delete_missing_task_returns_404(self, client) -> None:
        assert client.delete("/tasks/9999").status_code == 404


class TestCompleteTask:
    def test_marks_task_as_completed(self, client, sample_payload) -> None:
        created = client.post("/tasks", json=sample_payload).json()
        response = client.patch(f"/tasks/{created['id']}/complete")
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_complete_missing_task_returns_404(self, client) -> None:
        assert client.patch("/tasks/9999/complete").status_code == 404
