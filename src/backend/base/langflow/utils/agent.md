# utils/ — Shared Utilities

## Purpose
General-purpose utility functions used across the entire backend.

## Key Files

| File | Description |
|------|-------------|
| `async_helpers.py` | Async/await helper functions — running sync code in async contexts. |
| `compression.py` | Data compression utilities. |
| `concurrency.py` | Concurrency primitives — `KeyedMemoryLockManager` for fine-grained locking. |
| `connection_string_parser.py` | Database connection string parsing. |
| `constants.py` | Global constants. |
| `data_structure.py` | Data structure utilities. |
| `image.py` | Image processing utilities. |
| `lazy_load.py` | Lazy loading utilities for deferred imports. |
| `migration.py` | Database migration helper utilities. |
| `payload.py` | API payload construction utilities. |
| `schemas.py` | Utility Pydantic schemas. |
| `util.py` | General utility functions. |
| `util_strings.py` | String manipulation utilities. |
| `validate.py` | Validation functions. |
| `version.py` | Version checking — `get_version_info()`, `fetch_latest_version()`, `is_pre_release()`. |
| `voice_utils.py` | Voice/audio processing utilities. |

## For LLM Coding Agents

- Prefer adding to existing utility modules rather than creating new ones.
- Use `async_helpers.py` when bridging sync and async code.
- Use `concurrency.py` for thread-safe operations.
