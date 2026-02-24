# services/ — Service Layer

## Purpose
Implements the service-oriented architecture that provides infrastructure capabilities to the rest of the application. Services are managed by a central `ServiceManager` and accessed via dependency injection through `deps.py`. Each service follows a factory pattern: a `factory.py` creates the service instance, and a `service.py` implements the logic.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `auth/` | Authentication and authorization — JWT token management, user verification. |
| `cache/` | Caching service — in-memory and disk-based caching. |
| `chat/` | Chat service — manages chat sessions and message flow. |
| `database/` | Database service — SQLModel/SQLAlchemy ORM, connection management, and all data models. |
| `job_queue/` | Job queue service for background task management. |
| `session/` | Session management — tracks active flow execution sessions. |
| `settings/` | Application settings — configuration, feature flags, environment variables. |
| `shared_component_cache/` | Shared cache for component type definitions. |
| `socket/` | Socket.IO service for real-time WebSocket communication with the frontend. |
| `state/` | State service — runtime state management for flows. |
| `storage/` | File storage service — local filesystem and S3 backends. |
| `store/` | Langflow Store service — community component marketplace integration. |
| `task/` | Task service — background task scheduling (AnyIO and Celery backends). |
| `telemetry/` | Telemetry and OpenTelemetry instrumentation. |
| `tracing/` | Distributed tracing — LangSmith, LangFuse, LangWatch, Arize Phoenix, Opik integrations. |
| `variable/` | Variable/secret management — encrypted environment variable storage (DB and Kubernetes backends). |

## Key Files (at this level)

| File | Description |
|------|-------------|
| `manager.py` | `ServiceManager` — central registry that creates and manages all services via factories. |
| `base.py` | `Service` abstract base class. |
| `factory.py` | `ServiceFactory` abstract base class. |
| `deps.py` | FastAPI dependency injection functions — `get_db_service()`, `get_settings_service()`, `get_queue_service()`, etc. |
| `schema.py` | `ServiceType` enum listing all service types. |
| `utils.py` | Service initialization and teardown utilities — `initialize_services()`, `teardown_services()`. |

## Architecture Pattern

```
ServiceManager
  ├── registers ServiceFactory instances
  ├── creates Service instances on demand
  └── provides get(ServiceType) lookup

deps.py
  └── FastAPI Depends() functions that resolve services from the manager
```

## For LLM Coding Agents

- To add a new service: create a folder with `__init__.py`, `service.py`, `factory.py`, then register the factory in `manager.py`.
- Access services in API routes via `deps.py` dependency injection.
- All services implement `async def start()` and `async def stop()` lifecycle methods.
