# src/backend/base/langflow — Main Application Package

## Purpose
This is the root of the `langflow` Python package and the heart of the backend. It contains the FastAPI application factory, CLI entry point, graph execution engine, all built-in components, API routes, service infrastructure, and supporting utilities.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `alembic/` | Database migration scripts (Alembic). |
| `api/` | FastAPI route definitions (v1 and v2 endpoints). |
| `base/` | Abstract base classes for components (agents, models, tools, embeddings, etc.). |
| `components/` | Concrete component implementations that users drag onto the flow canvas. |
| `core/` | Celery app configuration for async task processing. |
| `custom/` | Custom component infrastructure — code parsing, component base classes, directory scanning. |
| `events/` | Event manager for publish/subscribe within graph execution. |
| `exceptions/` | Custom exception hierarchy (API errors, component errors, serialization errors). |
| `field_typing/` | Type constants and range specs for component input fields. |
| `graph/` | **Core graph execution engine** — edges, vertices, state management, scheduling. |
| `helpers/` | Helper functions for flows, users, folders, data manipulation. |
| `initial_setup/` | First-run setup — starter projects, super user creation, profile pictures. |
| `inputs/` | Input type definitions (StrInput, IntInput, DropdownInput, etc.) used by components. |
| `interface/` | Component type registry, dynamic import utilities, and LLM caching setup. |
| `io/` | I/O schema definitions for component inputs/outputs. |
| `legacy_custom/` | Legacy custom component support for backward compatibility. |
| `load/` | Flow loading and component instantiation utilities. |
| `logging/` | Loguru-based logging configuration with intercept handlers. |
| `processing/` | High-level flow orchestration — `run_graph_with_orchestrator()`. |
| `schema/` | Pydantic schemas for messages, data, artifacts, content blocks, graphs, playground events. |
| `serialization/` | Serialization/deserialization logic for flow data. |
| `services/` | Service layer — database, cache, auth, sessions, storage, tracing, telemetry, variables. |
| `template/` | Template engine for frontend node rendering — fields, frontend nodes, templates. |
| `type_extraction/` | Runtime type extraction from Python objects for component introspection. |
| `utils/` | Shared utilities — async helpers, compression, constants, validation, version checks. |

## Key Files (at this level)

| File | Role |
|------|------|
| `__init__.py` | Package init — exposes top-level imports. |
| `__main__.py` | CLI entry point (`python -m langflow`). Typer-based CLI with `run`, `superuser`, `migration`, and `io` commands. |
| `main.py` | FastAPI application factory — `setup_app()` creates the ASGI app with middleware, routes, and lifespan. |
| `server.py` | Gunicorn/Uvicorn worker classes for production deployment. |
| `worker.py` | Celery task definitions for async vertex building. |
| `memory.py` | LangChain memory key management utilities. |
| `middleware.py` | Content size limit middleware. |
| `settings.py` | Settings re-exports. |

## Execution Flow

1. `__main__.py` → parses CLI args → calls `setup_app()` from `main.py`
2. `main.py` → creates FastAPI app → registers routes from `api/router.py` → initializes services
3. Frontend sends flow JSON → `api/v1/chat.py` → `processing/orchestrator.py` → `graph/graph/base.py` (`Graph.arun()`)
4. Graph engine traverses vertices → each vertex runs its component → results stream back via Socket.IO

## For LLM Coding Agents

- **Adding a new component**: Create a file in `components/<category>/`, extend the appropriate base class from `base/`, export it in `__init__.py`.
- **Adding a new API endpoint**: Add a route in `api/v1/`, register it in `api/router.py`.
- **Modifying graph execution**: Work in `graph/graph/base.py` and `graph/graph/runnable_vertices_manager.py`.
- **Adding a new service**: Create a folder in `services/` with `service.py`, `factory.py`, register it in `services/manager.py`.
