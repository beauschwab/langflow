# AutoSys REST API Agent Tool: Research and Implementation Plan

## Executive summary
This document proposes a minimal-risk plan to add a new Langflow tool component that lets agents read and optionally trigger workloads through an AutoSys REST API. The approach keeps existing Langflow agent/tool UX unchanged and introduces the integration as a standard backend tool component under `components/tools/`.

## Repository locations reviewed
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/tools/search_api.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/tools/glean_search_api.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/tools/__init__.py`
- `/home/runner/work/langflow/langflow/docs/research/python-backend-langgraph-deep-dive.md`

## Current backend integration pattern (relevant findings)
1. Tool integrations are implemented as `LCToolComponent` classes in `src/backend/base/langflow/components/tools/`.
2. Each tool component defines:
   - typed `inputs` (including `SecretStrInput` for credentials),
   - a `build_tool()` method that returns a LangChain `StructuredTool`,
   - optional `run_model()` behavior for direct execution from canvas.
3. Tool registration/discovery is controlled through `components/tools/__init__.py`.

## AutoSys tool scope recommendation
### Phase 1 (MVP, read-focused)
- Add a single `AutoSysAPIComponent` with safe read operations:
  - list jobs by optional name filter,
  - get job status/details,
  - list recent runs/executions.
- Inputs:
  - `base_url` (AutoSys API endpoint),
  - `api_token` (secret),
  - `verify_ssl` (advanced, default true),
  - `timeout_seconds` (advanced, bounded int),
  - operation-specific fields (job name/id, status filter, limit).

### Phase 2 (controlled write operations)
- Add optional action endpoints only behind an explicit `allow_mutations` toggle:
  - start/force-start,
  - stop/terminate,
  - hold/release.
- Require explicit confirmation input (`confirm_action`) for mutation requests to reduce accidental agent actions.

## API/security design decisions
1. **Authentication:** Use bearer token via `Authorization: Bearer <token>`.
2. **Secrets handling:** Keep tokens in `SecretStrInput`; never log token values.
3. **Timeouts and retries:** enforce conservative timeout defaults and bounded retries for transient failures.
4. **Error sanitization:** map HTTP/network exceptions to user-safe error messages; do not expose raw stack traces or credential-bearing URLs.
5. **Least privilege:** document recommended read-only token for Phase 1 and separate elevated token for Phase 2 mutations.

## Proposed backend implementation tasks
1. Create `src/backend/base/langflow/components/tools/autosys_api.py`:
   - `AutoSysAPIComponent(LCToolComponent)`,
   - Pydantic args schema(s) for tool operations,
   - HTTP request helper with timeout + error normalization,
   - `StructuredTool` wrapper functions for each supported operation.
2. Register the component in `src/backend/base/langflow/components/tools/__init__.py`.
3. Add unit tests under `src/backend/tests/unit/components/tools/` for:
   - request construction and auth header behavior,
   - successful parsing of representative AutoSys responses,
   - timeout/network/4xx/5xx error mapping,
   - mutation guardrails (`allow_mutations`, `confirm_action`) once Phase 2 is added.

## Validation plan
1. Unit tests with mocked HTTP client responses (no live AutoSys dependency).
2. Manual smoke test from Langflow canvas:
   - attach tool to an agent,
   - run “list jobs” and “get job status” prompt,
   - verify structured outputs and user-safe failures.
3. Regression checks:
   - existing tool imports still resolve,
   - no changes to graph/orchestrator interfaces or API route contracts.

## Risks and mitigations
- **Risk:** API shape differences across AutoSys deployments/versions.
  - **Mitigation:** keep `base_url` configurable and isolate endpoint paths in constants; document tested versions.
- **Risk:** high-impact write actions invoked by autonomous agents.
  - **Mitigation:** deliver read-only MVP first, then gated mutation controls with explicit confirmation.
- **Risk:** secret leakage through logs/status fields.
  - **Mitigation:** avoid embedding headers/tokens in status; sanitize error outputs.

## Minimal rollout plan
1. Deliver Phase 1 read-only component and tests.
2. Gather user validation with real AutoSys environment.
3. Add Phase 2 mutation support only after guardrail review.
