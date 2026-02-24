# services/shared_component_cache/ — Shared Component Cache

## Purpose
Caches the component type definitions that are served to the frontend sidebar. Avoids recomputing the component registry on every request.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `SharedComponentCacheService` — caches component type dictionaries. |
| `factory.py` | `SharedComponentCacheServiceFactory`. |
