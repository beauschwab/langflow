# services/task/backends/ — Task Backends

## Purpose
Pluggable backend implementations for the task service.

## Key Files

| File | Description |
|------|-------------|
| `base.py` | Abstract task backend interface. |
| `anyio.py` | AnyIO-based in-process task backend (default). |
| `celery.py` | Celery-based distributed task backend for horizontal scaling. |
