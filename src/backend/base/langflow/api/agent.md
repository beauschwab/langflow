# api/ — FastAPI Route Definitions

## Purpose
Defines all HTTP API endpoints that the Langflow frontend and external clients consume. Routes are organized into versioned sub-packages (v1, v2) and mounted via the central `router.py`.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `v1/` | Version 1 API endpoints — the primary API surface. |
| `v2/` | Version 2 API endpoints — currently only contains an updated files endpoint. |
| `router.py` | Central APIRouter that mounts all v1 and v2 sub-routers under `/api/v1/` and `/api/v2/`. |
| `build.py` | Utilities for building/compiling flows via API. |
| `disconnect.py` | Endpoint for disconnecting active sessions. |
| `health_check_router.py` | `/health` endpoint for liveness/readiness probes. |
| `limited_background_tasks.py` | Rate-limited background task runner with semaphore control. |
| `log_router.py` | Endpoints for log streaming. |
| `schemas.py` | Shared Pydantic request/response schemas used across API routes. |
| `utils.py` | Shared API utilities (response formatting, error handling). |

## Key Functions

- `router` (in `router.py`): The main APIRouter instance imported by `main.py` and mounted on the FastAPI app.
- Health check endpoint provides `/health` for container orchestration.

## Frontend Integration

The React frontend makes HTTP requests to these endpoints for:
- Flow CRUD operations (`/api/v1/flows/`)
- Chat/build triggering (`/api/v1/chat/`, `/api/v1/build/`)
- Component type listing (`/api/v1/all`)
- User auth (`/api/v1/login/`, `/api/v1/users/`)
- File uploads (`/api/v1/files/`, `/api/v2/files/`)
- Store browsing (`/api/v1/store/`)
