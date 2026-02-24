# core/ — Celery Configuration

## Purpose
Celery application configuration for distributed task processing. Enables horizontal scaling by offloading vertex builds to worker processes.

## Key Files

| File | Description |
|------|-------------|
| `celery_app.py` | Creates and configures the Celery application instance. |
| `celeryconfig.py` | Celery configuration — broker URL, result backend, task serialization settings. |

## For LLM Coding Agents

- Celery is optional — the default backend uses AnyIO for in-process task execution.
- The Celery app is used by `worker.py` at the package root.
- Configure via `LANGFLOW_CELERY_BROKER_URL` and related environment variables.
