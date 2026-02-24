# alembic/versions/ — Migration Scripts

## Purpose
Contains individual Alembic migration scripts. Each file is auto-generated or manually created and represents a database schema change.

## For LLM Coding Agents

- Migration files are named with a revision hash prefix and a description.
- Each migration has `upgrade()` and `downgrade()` functions.
- Do not modify existing migrations — create new ones for schema changes.
