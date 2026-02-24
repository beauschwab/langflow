# services/task/ — Task Service

## Purpose
Background task scheduling with pluggable backends — AnyIO (in-process) and Celery (distributed).

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `backends/` | Task backend implementations. |
| `service.py` | `TaskService` — abstract task scheduling interface. |
| `factory.py` | `TaskServiceFactory`. |
| `temp_flow_cleanup.py` | Background task for cleaning up temporary flows. |
| `utils.py` | Task utility functions. |
