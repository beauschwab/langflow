# services/database/models/ — Database Models

## Purpose
SQLModel data model definitions for all database tables. Each subdirectory defines a model, its CRUD operations, and related schemas.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `agent/` | Agent model — stores agent configurations. |
| `api_key/` | API key model — stores user API keys with CRUD operations. |
| `file/` | File model — stores uploaded file metadata with CRUD operations. |
| `flow/` | Flow model — stores flow definitions (the JSON graph), with schemas and utilities. |
| `folder/` | Folder model — organizes flows into folders, with pagination support. |
| `message/` | Message model — stores chat messages with CRUD operations. |
| `tenant/` | Tenant model — multi-tenancy support. |
| `transactions/` | Transaction model — stores vertex build transaction records for monitoring. |
| `user/` | User model — stores user accounts with CRUD operations. |
| `variable/` | Variable model — stores encrypted environment variables. |
| `vertex_builds/` | Vertex build model — stores build results and timing data. |

## Key Files (at this level)

| File | Description |
|------|-------------|
| `base.py` | Base model class with common fields (id, timestamps). |

## For LLM Coding Agents

- All models use SQLModel (Pydantic + SQLAlchemy hybrid).
- CRUD operations are defined in `crud.py` files within each model folder.
- The `flow/model.py` is the most important model — it stores the entire flow graph JSON.
