# src/backend/base — Langflow Base Package

## Purpose
This is the root of the `langflow` Python package. It is installed as an editable package (`pip install -e .`) and contains all backend application code.

## Folder Structure

The single child folder is `langflow/`, which is the importable Python package. All submodules are documented in their own `agent.md` files within `langflow/`.

## Key Files

| File | Role |
|------|------|
| `pyproject.toml` | Package metadata, dependencies, and build configuration. Defines the `langflow` CLI entry point. |

## For LLM Coding Agents

- All source code lives under `langflow/`. Navigate there for any backend changes.
- When adding new dependencies, update `pyproject.toml` at this level.
