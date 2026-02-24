# tests/ — Frontend E2E & Integration Tests

## Purpose
Playwright-based end-to-end and integration tests for the Langflow frontend.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `core/` | Core test suites — features, integrations, regression tests, and unit tests. |
| `extended/` | Extended test suites — additional feature, integration, and regression tests. |
| `templates/` | Test template files and helpers. |
| `utils/` | Test utility functions and helpers. |
| `assets/` | Test assets (sample files, fixtures). |

## For LLM Coding Agents

- Tests use Playwright for browser automation.
- Run with `npx playwright test` from the frontend directory.
- Core tests cover essential functionality; extended tests cover edge cases.
