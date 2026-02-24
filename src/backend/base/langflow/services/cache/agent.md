# services/cache/ — Cache Service

## Purpose
Provides caching infrastructure with multiple backends — in-memory and disk-based caching.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `CacheService` — main cache service with get/set/delete operations. |
| `base.py` | Abstract cache backend interface. |
| `disk.py` | Disk-based cache backend using file system. |
| `factory.py` | `CacheServiceFactory` — selects cache backend based on configuration. |
| `utils.py` | Cache utility functions. |
