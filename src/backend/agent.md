# src/backend — Langflow Backend

## Purpose
This directory contains the entire Python backend for Langflow — a visual framework for building multi-agent and RAG applications. The backend is a FastAPI application that provides REST APIs consumed by the React frontend, a graph execution engine for running flows, and a service layer for persistence, caching, auth, and telemetry.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `base/` | The main Python package (`langflow`). Contains all application source code — API routes, component definitions, graph engine, services, schemas, and utilities. |
| `langflow/` | Lightweight package that exposes the Langflow version string. Used by packaging and the CLI `--version` flag. |
| `tests/` | Backend test suite — unit tests, integration tests, performance benchmarks, and load tests. Mirrors the `base/langflow/` module structure. |

## Key Files

| File | Role |
|------|------|
| `Dockerfile` | Multi-stage Docker build for the backend container image. |
| `.gitignore` | Backend-specific git ignore rules. |

## How It Integrates

- **Frontend → Backend**: The React frontend (`src/frontend/`) communicates with the backend exclusively through REST API endpoints defined in `base/langflow/api/`. WebSocket connections via Socket.IO are used for real-time streaming of build/chat events.
- **CLI**: `python -m langflow` invokes `base/langflow/__main__.py` which starts the FastAPI server via Uvicorn or Gunicorn.
- **Workers**: Celery workers (`base/langflow/worker.py`) can offload vertex builds to a task queue for horizontal scaling.

## For LLM Coding Agents

When modifying the backend:
1. API routes live in `base/langflow/api/` — start here when changing endpoint behavior.
2. Component logic lives in `base/langflow/components/` with base classes in `base/langflow/base/`.
3. Graph execution engine is in `base/langflow/graph/` — this is the core runtime.
4. Service infrastructure (database, cache, auth, etc.) is in `base/langflow/services/`.
5. Tests mirror the source tree under `tests/unit/` and `tests/integration/`.
