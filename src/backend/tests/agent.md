# tests/ — Backend Test Suite

## Purpose
Contains all backend tests — unit tests, integration tests, performance benchmarks, and load tests. Tests use pytest as the test framework with async support via pytest-asyncio.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `unit/` | Unit tests — organized to mirror the `base/langflow/` source structure. |
| `integration/` | Integration tests — tests that require external services or full application context. |
| `performance/` | Performance benchmark tests. |
| `locust/` | Load testing scripts using the Locust framework. |
| `data/` | Test data files (fixtures, sample flows, etc.). |
| `conftest.py` | Shared pytest fixtures — database setup, client creation, auth helpers. |
| `base.py` | Base test classes and utilities. |
| `constants.py` | Test constants. |
| `api_keys.py` | Test API key utilities. |

## For LLM Coding Agents

- Run tests with `pytest src/backend/tests/unit/` for unit tests.
- Use `pytest src/backend/tests/unit/path/to/test_file.py -k test_name` for specific tests.
- Tests use fixtures defined in `conftest.py` for database sessions, API clients, and auth.
- When adding new backend functionality, add corresponding tests in the matching unit test directory.
