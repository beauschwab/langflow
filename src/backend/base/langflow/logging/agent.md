# logging/ — Logging Configuration

## Purpose
Loguru-based logging setup with intercept handlers for capturing logs from third-party libraries (uvicorn, gunicorn, etc.).

## Key Files

| File | Description |
|------|-------------|
| `logger.py` | `configure()` function — sets up loguru with appropriate sinks, formats, and log levels. `InterceptHandler` — redirects standard library `logging` to loguru. |
| `setup.py` | Additional logging setup utilities. |

## For LLM Coding Agents

- Use `from loguru import logger` for all logging — do not use `import logging`.
- Log levels and formats are configured via settings.
