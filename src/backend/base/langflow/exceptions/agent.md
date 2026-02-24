# exceptions/ — Custom Exception Hierarchy

## Purpose
Defines custom exception classes used throughout the backend for structured error handling.

## Key Files

| File | Description |
|------|-------------|
| `api.py` | API-level exceptions — HTTP error responses with status codes. |
| `component.py` | Component exceptions — `ComponentBuildError` and related errors during component execution. |
| `serialization.py` | Serialization exceptions — errors during data serialization/deserialization. |
