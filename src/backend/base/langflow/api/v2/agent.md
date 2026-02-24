# api/v2/ — Version 2 API Endpoints

## Purpose
Contains updated API endpoints that supersede or extend v1 functionality. Currently minimal — only an updated files endpoint.

## Key Files

| File | Description |
|------|-------------|
| `files.py` | Updated file upload/download endpoint with improved handling. |
| `__init__.py` | Exports the v2 files router. |

## For LLM Coding Agents

- When adding new endpoints that break v1 compatibility, add them here as v2.
- The v2 router is mounted at `/api/v2/` by `api/router.py`.
