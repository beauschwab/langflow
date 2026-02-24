# api/v1/ — Version 1 API Endpoints

## Purpose
Contains all v1 REST API route handlers. This is the primary API surface consumed by the Langflow frontend and third-party integrations.

## Key Files

| File | Description |
|------|-------------|
| `chat.py` | Chat/build endpoints — triggers flow execution and streams results via SSE. Entry point for `run_graph_internal()`. |
| `flows.py` | Flow CRUD — create, read, update, delete, import, export flows. Supports JSON and YAML formats. |
| `folders.py` | Folder management for organizing flows. |
| `endpoints.py` | Component type listing (`/all`) — returns all available component types for the flow editor sidebar. |
| `login.py` | Authentication endpoints — login, auto-login, refresh tokens. |
| `users.py` | User management — create, update, delete users. |
| `api_key.py` | API key CRUD for programmatic access. |
| `files.py` | File upload/download endpoints. |
| `monitor.py` | Message and transaction monitoring endpoints. |
| `store.py` | Langflow Store integration — browse and install community components. |
| `variable.py` | Environment variable management (stored encrypted). |
| `validate.py` | Code validation endpoints for custom components. |
| `starter_projects.py` | Starter/template project endpoints. |
| `agents.py` | Agent-specific API endpoints. |
| `a2a.py` | Agent-to-Agent (A2A) protocol endpoints. |
| `mcp.py` | Model Context Protocol (MCP) server endpoint. |
| `callback.py` | Callback URL endpoints for async notifications. |
| `base.py` | Shared base utilities for v1 routes. |
| `schemas.py` | V1-specific Pydantic request/response schemas. |

## Key Functions

- `build_flow()` in `chat.py`: Main entry point for executing a flow — receives flow JSON, builds the graph, runs it, and streams events.
- `read_flows()`, `create_flow()`, `update_flow()`, `delete_flow()` in `flows.py`: Standard CRUD for flows.
- `LoginHandler` in `login.py`: Issues JWT access/refresh tokens.

## Frontend Integration

Every panel, dialog, and action in the React frontend maps to one or more v1 endpoints:
- Flow editor saves → `PUT /api/v1/flows/{flow_id}`
- Chat interaction → `POST /api/v1/build/{flow_id}/flow`
- Sidebar component list → `GET /api/v1/all`
- Login → `POST /api/v1/login`
