# services/variable/ — Variable/Secret Management Service

## Purpose
Manages encrypted environment variables and secrets. Supports database storage and Kubernetes Secrets backends.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `VariableService` — CRUD operations for encrypted variables. |
| `base.py` | Abstract variable storage interface. |
| `factory.py` | `VariableServiceFactory`. |
| `constants.py` | Variable-related constants. |
| `kubernetes.py` | Kubernetes Secrets backend. |
| `kubernetes_secrets.py` | Kubernetes Secrets helper utilities. |

## For LLM Coding Agents

- Variables are encrypted at rest in the database.
- The Kubernetes backend stores secrets in K8s Secret resources instead of the database.
