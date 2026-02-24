# alembic/ — Database Migrations

## Purpose
Alembic migration scripts for evolving the database schema. Alembic is configured via `alembic.ini` at the langflow package root.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `versions/` | Individual migration scripts — each file represents a schema change with `upgrade()` and `downgrade()` functions. |

## For LLM Coding Agents

- Run `alembic revision --autogenerate -m "description"` to create new migrations after modifying SQLModel definitions.
- Migrations are applied automatically on startup via the database service.
- Never manually edit existing migration files — create new ones instead.
