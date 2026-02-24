# services/session/ — Session Service

## Purpose
Manages active flow execution sessions — tracks which flows are currently running and their state.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `SessionService` — creates, retrieves, and cleans up flow execution sessions. |
| `factory.py` | `SessionServiceFactory`. |
| `utils.py` | Session utility functions. |
