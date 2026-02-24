# services/database/ — Database Service

## Purpose
Database connectivity and ORM layer using SQLModel (SQLAlchemy). Manages database connections, sessions, and hosts all data model definitions.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `models/` | SQLModel data model definitions for all database tables. |
| `service.py` | `DatabaseService` — manages the SQLAlchemy engine, session factory, and database lifecycle. |
| `factory.py` | `DatabaseServiceFactory`. |
| `utils.py` | Database utility functions — `session_getter()` context manager, migration helpers. |

## Key Concepts

- Uses SQLModel (Pydantic + SQLAlchemy) for type-safe ORM.
- Default database is SQLite; PostgreSQL is supported for production.
- Alembic handles schema migrations (see `alembic/` at the langflow root level).
