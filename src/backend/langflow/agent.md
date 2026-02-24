# src/backend/langflow — Version Package

## Purpose
Minimal package that provides the Langflow version string. This is a separate package from `base/langflow/` and exists solely for version management.

## Key Files

| File | Role |
|------|------|
| `version/` | Contains the version number used by `langflow --version` and packaging tools. |

## For LLM Coding Agents

- You rarely need to modify this directory. Version bumps are handled by the release process.
- The main application code is in `src/backend/base/langflow/`, not here.
