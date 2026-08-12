# task-management-api
Simple Task Managemen API — Software Engineering project

## Stack

- Python
- FastAPI
- PostgreSQL
- pytest
- Docker
- Github Actions

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{task_id}` | Retrieve a single task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| PATCH | `/tasks/{task_id}/complete` | Mark a task as completed |

## Project Structure

```text
task-management-api/
├── app/                  # FastAPI application
├── tests/                # pytest test suite
├── .github/workflows/    # CI configuration
├── Dockerfile            # API container image
├── compose.yaml          # api + postgres stack
├── requirements.txt      # Python dependencies
├── .dockerignore
├── .gitignore
└── README.md
