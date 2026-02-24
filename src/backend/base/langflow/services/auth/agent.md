# services/auth/ — Authentication Service

## Purpose
Manages authentication and authorization — JWT token creation/validation, password hashing, and user verification.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `AuthService` — creates/validates JWT access and refresh tokens, hashes/verifies passwords. |
| `factory.py` | `AuthServiceFactory` — creates the auth service instance. |
| `utils.py` | Auth utility functions — token extraction from requests, user lookup. |

## Frontend Integration

- Login endpoint issues JWT tokens consumed by the frontend.
- All authenticated API requests include the JWT in the Authorization header.
