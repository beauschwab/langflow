# SharePoint Files Access Component: Research and Implementation Plan

## Executive Summary
This document proposes a new Langflow component for accessing files stored in Microsoft SharePoint and OneDrive for Business through Microsoft Graph. The goal is to provide enterprise teams with a first-class document ingestion path that matches existing loader-style components (for example, Google Drive and Confluence) while preserving current Langflow component patterns and flow semantics.

Recommended initial scope is a **read-only SharePoint Files Loader** that supports listing and loading document content/metadata from a configured site and document library path.

## Repository locations reviewed
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/google/google_drive.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/confluence/confluence.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/Notion/search.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/Notion/page_content_viewer.py`
- `/home/runner/work/langflow/langflow/docs/research/python-backend-langgraph-deep-dive.md`
- `/home/runner/work/langflow/langflow/docs/research/enterprise-data-access-controls-langgraph-assessment.md`

## Current-state findings
- There is no existing SharePoint-specific component in the current component catalog.
- Existing enterprise document integrations in this repository generally follow:
  1. `Component` subclass with typed inputs/outputs.
  2. Credential inputs via `SecretStrInput`.
  3. Return values normalized as `Data` or `list[Data]`.
  4. Provider-specific loader/client usage behind a small `build_*` helper method.

## Proposed component (Phase 1 target)
### Component identity
- **Display name:** `SharePoint Files Loader`
- **Category:** document loaders / enterprise data access
- **Primary output:** `list[Data]`

### Inputs (initial)
- `tenant_id` (required, text)
- `client_id` (required, secret/text)
- `client_secret` (required, secret)
- `site_hostname` (required, text; example: `contoso.sharepoint.com`)
- `site_path` (required, text; example: `/sites/FinanceOps`)
- `library_name` (optional, default `Documents`)
- `folder_path` (optional; load all files when omitted)
- `recursive` (optional bool; default `true`)
- `max_files` (optional int; bounded for safe execution)
- `file_types` (optional text list/filter)

### Output shape
- `Data.text`: extracted document text (when extractable)
- `Data.data`: structured metadata at minimum including `source`, `file_name`, `web_url`, `site_id`, `drive_id`, `item_id`, `last_modified`, `mime_type`

## Architecture approach
### API strategy
- Use Microsoft Graph REST endpoints for sites/drives/items traversal and file content retrieval.
- Keep Graph client details internal to the component and expose only Langflow-native inputs/outputs.

### Component pattern alignment
- Mirror the small-surface style used by `google_drive.py` and `confluence.py`:
  - one builder method for client setup,
  - one load method for retrieval + normalization to `Data`,
  - explicit validation/error messages for missing or invalid inputs.

### Orchestration compatibility
- Component remains a standard Langflow node and does not require orchestration changes.
- Works in both legacy and langgraph backend execution modes because it conforms to existing component contracts.

## Security and enterprise requirements
- Use app-only OAuth credentials (client credentials grant) for service-to-service access.
- Never log raw secrets or tokens.
- Sanitize provider errors before surfacing to users.
- Respect least privilege: recommend read-only Graph scopes for initial implementation.
- Include timeout and bounded file retrieval (`max_files`) to reduce denial-of-service risk from large libraries.

## Implementation plan
### Phase 1: Read-only loader MVP
1. Add a new backend component module under `src/backend/base/langflow/components/` (SharePoint-specific folder).
2. Implement site/library/folder listing and file download via Graph.
3. Normalize results into `list[Data]` with consistent metadata.
4. Add targeted unit tests for input validation, API paging handling, and output normalization.

### Phase 2: Content and filtering enhancements
1. Add richer MIME-type handling and optional per-file size caps.
2. Improve include/exclude patterns for folders and extensions.
3. Add optional incremental mode using last-modified timestamps.

### Phase 3: Enterprise hardening
1. Add clearer retry/backoff behavior for Graph throttling.
2. Add tenant-scope validation checks and better diagnostics for misconfigured sites/libraries.
3. Add documentation for required Azure app registration and minimal permission sets.

## Test and validation plan
- Unit tests:
  - missing/invalid credentials and identifiers,
  - empty results behavior,
  - pagination and `max_files` limits,
  - metadata mapping to `Data`.
- Integration-style tests (mocked HTTP or recorded fixtures):
  - site lookup, drive lookup, folder traversal, content retrieval.
- Manual verification:
  - run a flow with the component and verify deterministic `Data` output shape.

## Open questions before implementation
- Whether to support delegated authentication in addition to app-only authentication for tenant policies that block app-only access.
- Which file parsers should be bundled for non-text binary formats in MVP vs follow-up.
- Whether SharePoint permissions should be validated pre-run (fast-fail) or lazily during traversal.
