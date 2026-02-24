# components/authorization/ — Auth Guard Components

## Purpose
Route guard components that protect pages based on authentication status and user roles.

## Subdirectories

| Folder | Description |
|--------|-------------|
| `authAdminGuard/` | Guards admin-only routes — redirects non-admin users. |
| `authGuard/` | Guards authenticated routes — redirects unauthenticated users to login. |
| `authLoginGuard/` | Guards login page — redirects already-authenticated users away. |
| `authSettingsGuard/` | Guards settings pages. |
| `storeGuard/` | Guards store-related routes. |
