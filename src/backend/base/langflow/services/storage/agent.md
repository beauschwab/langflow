# services/storage/ — File Storage Service

## Purpose
File storage abstraction with pluggable backends — local filesystem and AWS S3.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `StorageService` abstract interface — save, load, delete files. |
| `local.py` | Local filesystem storage backend. |
| `s3.py` | AWS S3 storage backend. |
| `factory.py` | `StorageServiceFactory` — selects backend based on configuration. |
| `constants.py` | Storage constants (paths, limits). |
| `utils.py` | Storage utility functions. |
